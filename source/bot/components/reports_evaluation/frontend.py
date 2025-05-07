from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery

from components.main_menu.frontend import frontend_cb_mm_main, frontend_cmd_mm_start
from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)
from components.reports_evaluation.fsm_states import REAuthStates, REEvaluationStates
from components.reports_evaluation.keyboards import (
    re_get_main_menu_keyboard,
    re_get_presentations_keyboard,
    re_get_criterion_keyboard,
    re_get_final_score_keyboard,
    re_get_commentary_keyboard,
    re_get_auth_continue_keyboard,
)
from components.reports_evaluation.utils import (
    re_check_access_code,
    re_require_auth,
    getstr,
    re_add_auth_message,
    re_delete_auth_messages,
)


async def frontend_cb_re_auth(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Shows user prompt for entering access code.
    """
    # TODO: Add reply button to return to main_menu
    await state.clear()
    lang = "ru"

    await state.set_state(REAuthStates.waiting_for_code)

    msg = await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.auth.caption")
    )

    await re_add_auth_message(state, msg.message_id)


async def frontend_st_re_process_code(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    """
    Handles juror authorization based on input code.
    - On success: stores code, sets state, shows main menu.
    - On failure: shows error message with a back button.
    """
    lang = "ru"
    code = message.text.strip()

    # Save user message
    await re_add_auth_message(state, message.message_id)

    juror = await re_check_access_code(code)

    if juror:
        await state.update_data(jury_code=code)
        await state.set_state(REAuthStates.authorized)

        caption, keyboard = re_get_auth_continue_keyboard(lang)

        await message.answer(
            text=caption,
            reply_markup=keyboard,
        )
    else:
        # Save invalid code message for deletion
        msg = await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"))
        await re_add_auth_message(state, msg.message_id)


@re_require_auth
async def frontend_cb_re_main_menu(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles showing main menu of reports evaluation.
    """
    lang = "ru"
    state_data = await state.get_data()

    # Delete auth messages
    if "re_auth_message_ids" in state_data:
        print("here")
        await re_delete_auth_messages(state, callback_query.message.chat.id, bot)

    jury_code = state_data.get("jury_code")
    jury_name = PLACEHOLDER_JURY[jury_code]["name"]

    keyboard = re_get_main_menu_keyboard(lang)
    await callback_query.message.edit_text(
        getstr(lang, "reports_evaluation.menu.caption").format(jury_name=jury_name),
        reply_markup=keyboard,
    )


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
    juror_code = data["jury_code"]

    # Fetch the presentations and generate the keyboard with the appropriate page
    caption, keyboard = re_get_presentations_keyboard(
        lang, PLACEHOLDER_PRESENTS, juror_code, page
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
async def frontend_cb_re_choose_presentation(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles starting of report evaluation.
    """
    lang = "ru"

    pres_id = callback_query.data.split(":")[1]
    await state.update_data(
        {
            "pres_id": pres_id,
            "scores": {},
        }
    )
    caption, keyboard = re_get_criterion_keyboard(lang, "organization")

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_handle_eval_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles score selection for a given criterion during evaluation.
    Saves the score in FSM state and moves to the next criterion, or finalizes if it's the last one.
    """
    lang = "ru"

    _, criterion, value = callback_query.data.split(":")
    value = int(value)

    data = await state.get_data()
    scores = dict(data.get("scores", {}))
    scores[criterion] = value
    await state.update_data(scores=scores)

    # Check if the current criterion is the last one
    next_criterion_idx = EVAL_CRITERIA.index(criterion) + 1
    if next_criterion_idx >= len(EVAL_CRITERIA):
        await frontend_re_finalize_score(callback_query, bot, state)
        return

    # Show next criterion
    next_criterion = EVAL_CRITERIA[next_criterion_idx]
    caption, keyboard = re_get_criterion_keyboard(lang, next_criterion)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_cb_re_return_to_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Handles navigation back to a previously scored criterion.
    Resets the score in state and re-displays the evaluation keyboard for that criterion.
    """
    lang = "ru"

    criterion = callback_query.data.split(":")[1]

    data = await state.get_data()
    scores = dict(data.get("scores", {}))
    scores[criterion] = ""
    await state.update_data(scores=scores)

    caption, keyboard = re_get_criterion_keyboard(lang, criterion)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_re_finalize_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Final step of the evaluation: checks if all criteria are scored and shows the summary with action buttons.
    """
    lang = "ru"

    data = await state.get_data()
    scores = dict(data.get("scores", {}))
    pres_id = data.get("pres_id")
    print(f"[DEBUG] {scores}")

    # # Check if all criteria are in place
    # missing = [criterion for criterion in EVAL_CRITERIA if criterion not in scores]
    # if missing:
    #     await callback_query.answer(
    #         text="Что-то пошло не так. Попробуйте снова.", show_alert=True
    #     )
    #     await frontend_cb_mm_main(callback_query, bot)
    #     return

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

    caption, keyboard = re_get_commentary_keyboard(lang)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


# TODO: Change placeholders to db change
async def re_submit_scores(state: FSMContext, comments: str = ""):
    """
    Stores the submitted scores and optional comments into the PLACEHOLDER_PRESENTS data structure.
    Finds the presentation by ID and attaches the scores by juror ID.
    """
    data = await state.get_data()
    scores = dict(data.get("scores", {}))
    pres_id = data.get("pres_id")
    juror_id = data.get("jury_code")

    if not all([pres_id, juror_id, scores]):
        print("[ERROR] Missing data in state")
        print(f"[DEBUG] {scores}, {pres_id}, {juror_id}")
        return

    # Set scores
    for pres in PLACEHOLDER_PRESENTS:
        if pres["id"] == pres_id:
            pres["jury_scores"][juror_id] = scores
            if comments.strip():
                pres["comments"][juror_id] = comments.strip()
            print(f"[DEBUG] Updated presentation: {pres}")
            break
    else:
        print(f"[ERROR] Presentation {pres_id} not found")


@re_require_auth
async def frontend_cb_re_skip_comments(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Finalizes the evaluation when the reviewer chooses to skip adding comments.
    Calls score submission logic and returns to the main menu.
    """
    lang = "ru"

    await re_submit_scores(state)

    await callback_query.message.answer(
        text=getstr(lang, "reports_evaluation.evaluation.marks_accepted"),
    )
    # TODO: Placeholder
    await frontend_cb_mm_main(callback_query, bot)


async def frontend_st_re_eval_comment(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    """
    Handles user-submitted comments after scoring.
    Stores the comment alongside the scores and returns to the main menu.
    """
    lang = "ru"

    commentary = message.text
    print(f"[DEBUG] {commentary}")

    await re_submit_scores(state, commentary)

    await message.answer(
        text=getstr(lang, "reports_evaluation.evaluation.marks_accepted"),
    )
    # TODO: Placeholder
    # Should offer the ability to continue to cb_re_main_menu or change the commentary.
    await frontend_cmd_mm_start(message, bot)
