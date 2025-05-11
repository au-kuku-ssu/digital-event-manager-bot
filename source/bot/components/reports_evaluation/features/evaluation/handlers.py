from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.features.evaluation.keyboards import (
    re_get_presentations_keyboard,
    re_get_criterion_keyboard,
    re_get_final_score_keyboard,
    re_get_comment_keyboard,
    re_get_marks_accepted_keyboard,
    re_get_comment_check_keyboard,
    re_get_error_keyboard,
)
from components.reports_evaluation.fsm_states import REEvaluationStates
from components.reports_evaluation.services.evaluation import (
    re_submit_scores,
    re_finalize_score,
)
from components.reports_evaluation.utils import getstr, re_require_auth


@re_require_auth
async def frontend_cb_re_show_presentations(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing presentation keyboard.
    """
    lang = "ru"
    page = int(callback_query.data.split(":")[1])

    data = await state.get_data()
    jury_code = data["jury_code"]

    # Fetch the presentations and generate the keyboard with the appropriate page
    caption, keyboard = re_get_presentations_keyboard(
        lang, PLACEHOLDER_PRESENTS, jury_code, page
    )

    # If no presents available
    if not caption:
        await callback_query.message.edit_text(
            text=getstr(lang, "reports_evaluation.presents.no_presents_available"),
            reply_markup=keyboard,
        )
        return

    # Update the message with the new caption and keyboard
    await callback_query.message.edit_text(
        text=caption, reply_markup=keyboard, parse_mode="HTML"
    )


@re_require_auth
async def frontend_cb_re_eval_choose_presentation(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles starting of report evaluation.
    """
    lang = "ru"

    pres_id = callback_query.data.split(":")[1]
    # Set pres_id, scores to state data
    await state.update_data(pres_id=pres_id, scores={})
    caption, keyboard = re_get_criterion_keyboard(lang, pres_id, "organization")

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_eval_handle_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles score selection for a given criterion during evaluation.
    Saves the score in FSM state and moves to the next criterion, or finalizes if it's the last one.
    """
    lang = "ru"

    _, pres_id, criterion, value = callback_query.data.split(":")
    value = int(value)

    data = await state.get_data()

    # Check if pres_id from callback and state data are different
    state_pres_id = data["pres_id"]
    if pres_id != state_pres_id:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)

        caption, keyboard = re_get_error_keyboard(lang)
        await callback_query.message.edit_text(
            text=caption,
            reply_markup=keyboard,
        )
        return

    scores = dict(data.get("scores") or {})
    scores[criterion] = value
    await state.update_data(scores=scores)

    # Check if the current criterion is the last one
    next_criterion_idx = EVAL_CRITERIA.index(criterion) + 1
    if next_criterion_idx >= len(EVAL_CRITERIA):
        await frontend_re_eval_finalize_score(callback_query, bot, state)
        return

    # Show next criterion
    next_criterion = EVAL_CRITERIA[next_criterion_idx]
    caption, keyboard = re_get_criterion_keyboard(lang, pres_id, next_criterion)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_cb_re_eval_return_to_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles navigation back to a previously scored criterion.
    Resets the score in state and re-displays the evaluation keyboard for that criterion.
    """
    lang = "ru"

    _, pres_id, criterion = callback_query.data.split(":")

    data = await state.get_data()

    # Check if pres_id from callback and state data are different
    state_pres_id = data["pres_id"]
    if pres_id != state_pres_id:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)

        caption, keyboard = re_get_error_keyboard(lang)
        await callback_query.message.edit_text(
            text=caption,
            reply_markup=keyboard,
        )
        return

    scores = dict(data.get("scores") or {})
    scores[criterion] = ""
    await state.update_data(scores=scores)

    caption, keyboard = re_get_criterion_keyboard(lang, pres_id, criterion)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_re_eval_finalize_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Final step of the evaluation: checks if all criteria are scored and shows the summary with action buttons.
    """
    lang = "ru"

    # Check if there are problems with scores
    is_scores_ok = await re_finalize_score(state)
    if not is_scores_ok:
        caption, keyboard = re_get_error_keyboard(lang)

        await state.update_data(scores=None, pres_id=None, pres_comments=None)

        await callback_query.message.edit_text(
            text=caption,
            reply_markup=keyboard,
        )
        return

    data = await state.get_data()
    scores = data.get("scores", {})
    pres_id = data.get("pres_id")
    # print(f"[DEBUG] {scores}")

    caption, keyboard = re_get_final_score_keyboard(lang, scores, pres_id)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_cb_re_eval_comment(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Switches FSM to the comment input state after all scores are submitted.
    Prompts user to leave optional feedback for the evaluated presentation.
    """
    lang = "ru"

    await state.set_state(REEvaluationStates.waiting_for_comment)
    await state.update_data(pres_comments=None)

    caption, keyboard = re_get_comment_keyboard(lang)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


async def frontend_st_re_eval_comment(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    """
    Handles user-submitted comments after scoring.
    Stores the comment alongside the scores and returns to the main menu.
    """
    lang = "ru"

    comment = message.text.strip()
    await state.set_state(REEvaluationStates.comment_added)
    await state.update_data(pres_comments=comment)

    caption, keyboard = re_get_comment_check_keyboard(lang, comment)

    await message.answer(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_eval_marks_accepted(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Finalizes the evaluation when the reviewer chooses to skip comments or adds them.
    Calls score submission logic and returns to the main menu.
    """
    lang = "ru"

    await state.set_state(REEvaluationStates.marks_accepted)
    marks_state = await re_submit_scores(state)

    caption, keyboard = re_get_marks_accepted_keyboard(lang, marks_state)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
