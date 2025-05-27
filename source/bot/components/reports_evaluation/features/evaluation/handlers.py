from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
import logging

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
from components.shared.db import Database


@re_require_auth
async def frontend_cb_re_show_presentations(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles showing presentation keyboard.
    """
    lang = "ru"
    page = int(callback_query.data.split(":")[1])

    data = await state.get_data()
    auth_code = data.get("auth_code")

    if not auth_code:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no auth code")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    # Fetch the presentations and generate the keyboard with the appropriate page
    caption, keyboard = re_get_presentations_keyboard(
        lang, PLACEHOLDER_PRESENTS, auth_code, page
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
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles starting of report evaluation.
    """
    lang = "ru"

    pres_id_from_callback = callback_query.data.split(":")[1]
    # Set pres_id, scores, pres_comments to state data

    data = await state.get_data()
    existing_pres_id = data.get("pres_id")

    if existing_pres_id:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "parallel scoring")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    await state.update_data(
        pres_id=pres_id_from_callback, scores={}, pres_comments=None
    )

    first_criterion = EVAL_CRITERIA[0] if EVAL_CRITERIA else None
    if not first_criterion:
        caption_err, keyboard_err = re_get_error_keyboard(
            lang, "no criterion available"
        )
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    caption, keyboard = re_get_criterion_keyboard(
        lang, pres_id_from_callback, "organization"
    )

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_eval_handle_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles score selection for a given criterion during evaluation.
    Saves the score in FSM state and moves to the next criterion, or finalizes if it's the last one.
    """
    lang = "ru"

    _, criterion, value = callback_query.data.split(":")
    value = int(value)

    data = await state.get_data()
    current_pres_id = data.get("pres_id")
    actor_auth_code = data.get("auth_code") 
    actor_is_chairman = data.get("is_chairman", False)

    # --- Chair Edit Mode Logic ---
    editing_target_access_key = data.get("editing_target_access_key", None)
    # --- End Chair Edit Mode Logic ---

    if not current_pres_id or not actor_auth_code:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no current pres id or auth code")
        await callback_query.message.edit_text(text=caption_err, reply_markup=keyboard_err)
        return

    actor_jury_id = await db.get_jury_id_by_access_key(actor_auth_code)
    if not actor_jury_id:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "actor jury id not found")
        await callback_query.message.edit_text(text=caption_err, reply_markup=keyboard_err)
        return

    target_jury_id_for_score = actor_jury_id
    editor_jury_id_for_log = None
    is_effective_chair_edit = False

    if actor_is_chairman and editing_target_access_key:
        if editing_target_access_key == actor_auth_code:
            # Chairman editing their own scores, not a "chair edit" in the special sense
            pass # target_jury_id_for_score is already actor_jury_id
        else:
            # Chairman is editing another juror's scores
            target_juror_id_being_edited = await db.get_jury_id_by_access_key(editing_target_access_key)
            if not target_juror_id_being_edited:
                caption_err, keyboard_err = re_get_error_keyboard(lang, "target juror for edit not found")
                await callback_query.message.edit_text(text=caption_err, reply_markup=keyboard_err)
                return
            target_jury_id_for_score = target_juror_id_being_edited
            editor_jury_id_for_log = actor_jury_id # The chairman is the editor
            is_effective_chair_edit = True

    try:
        participant_id = int(current_pres_id)
    except ValueError:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid pres id format")
        await callback_query.message.edit_text(text=caption_err, reply_markup=keyboard_err)
        return
    
    await db.save_score(
        jury_id=target_jury_id_for_score, 
        participant_id=participant_id, 
        criterion=criterion, 
        value=float(value),
        editor_jury_id=editor_jury_id_for_log,
        is_chair_edit=is_effective_chair_edit
    )

    try:
        current_criterion_idx = EVAL_CRITERIA.index(criterion)
    except ValueError:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid criterion")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    next_criterion_idx = current_criterion_idx + 1
    if next_criterion_idx >= len(EVAL_CRITERIA):
        await frontend_re_eval_finalize_score(callback_query, bot, state, db)
        return

    next_criterion = EVAL_CRITERIA[next_criterion_idx]
    caption, keyboard = re_get_criterion_keyboard(lang, current_pres_id, next_criterion)
    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_eval_return_to_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles navigation back to a previously scored criterion.
    Resets the score in state and re-displays the evaluation keyboard for that criterion.
    """
    lang = "ru"

    _, criterion = callback_query.data.split(":")

    data = await state.get_data()
    current_pres_id = data.get("pres_id")
    auth_code = data.get("auth_code")

    if not current_pres_id or not auth_code:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no current pres id or auth code")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    jury_id = await db.get_jury_id_by_access_key(auth_code)
    if not jury_id:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "jury id not found")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return
    
    try:
        participant_id = int(current_pres_id)
    except ValueError:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid pres id format")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    if criterion not in EVAL_CRITERIA:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid criterion")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    # Nullify score in DB
    await db.delete_score(jury_id, participant_id, criterion)

    caption, keyboard = re_get_criterion_keyboard(lang, current_pres_id, criterion)
    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_re_eval_finalize_score(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Final step of the evaluation: checks if all criteria are scored and shows the summary with action buttons.
    """
    lang = "ru"

    data = await state.get_data()
    pres_id = data.get("pres_id")
    auth_code = data.get("auth_code")
    editing_target_access_key = data.get("editing_target_access_key", None)

    if not pres_id or not auth_code:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "missing pres_id or auth_code")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return
    
    if editing_target_access_key:
        jury_id = await db.get_jury_id_by_access_key(editing_target_access_key)
    else:
        jury_id = await db.get_jury_id_by_access_key(auth_code)

    if not jury_id:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "jury id not found")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    try:
        participant_id = int(pres_id)
    except ValueError:
        await state.update_data(scores=None, pres_id=None, pres_comments=None)
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid pres id format")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    scores = await db.get_scores(jury_id, participant_id)

    # Check if there are problems with scores
    # The re_finalize_score service might need adjustment to accept scores as a parameter
    # or fetch them itself if it has access to db and necessary ids.
    # For now, passing scores directly.
    is_scores_ok = await re_finalize_score(scores) # Pass scores to the service function
    if not is_scores_ok:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "missing criteria")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    caption, keyboard = re_get_final_score_keyboard(lang, scores, pres_id)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@re_require_auth
async def frontend_cb_re_eval_comment(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Switches FSM to the comment input state after all scores are submitted.
    Prompts user to leave optional feedback for the evaluated presentation.
    """
    lang = "ru"

    data = await state.get_data()
    pres_id = data.get("pres_id")
    auth_code = data.get("auth_code")

    if not pres_id or not auth_code:
        caption_err, keyboard_err = re_get_error_keyboard(
            lang, "missing pres_id or auth_code"
        )
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    jury_id = await db.get_jury_id_by_access_key(auth_code)
    if not jury_id:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "jury id not found")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    try:
        participant_id = int(pres_id)
    except ValueError:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid pres id format")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    scores = await db.get_scores(jury_id, participant_id)

    if not scores:
        caption_err, keyboard_err = re_get_error_keyboard(
            lang, "missing scores in db for comment"
        )
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    # Set state for comment waiting
    await state.set_state(REEvaluationStates.waiting_for_comment)

    caption, keyboard = re_get_comment_keyboard(lang)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )


async def frontend_st_re_eval_comment(
    message: types.Message, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Handles user-submitted comments after scoring.
    Stores the comment alongside the scores and returns to the main menu.
    """
    lang = "ru"

    comment = message.text.strip()
    await state.set_state(None)
    await state.update_data(pres_comments=comment)

    caption, keyboard = re_get_comment_check_keyboard(lang, comment)

    await message.answer(
        text=caption,
        reply_markup=keyboard,
    )


@re_require_auth
async def frontend_cb_re_eval_marks_accepted(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """
    Finalizes the evaluation when the reviewer chooses to skip comments or adds them.
    Calls score submission logic and returns to the main menu.
    """
    lang = "ru"

    data = await state.get_data()
    pres_id = data.get("pres_id")
    auth_code = data.get("auth_code")

    if not pres_id or not auth_code:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no pres id or auth code")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    jury_id = await db.get_jury_id_by_access_key(auth_code)
    if not jury_id:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "jury id not found")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    try:
        participant_id = int(pres_id)
    except ValueError:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "invalid pres id format")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    scores = await db.get_scores(jury_id, participant_id)
    if not scores:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no scores in db")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )
        return

    await state.set_state(REEvaluationStates.marks_accepted)
    marks_state = await re_submit_scores(state, db, jury_id, participant_id, scores)

    if not marks_state:
        caption_err, keyboard_err = re_get_error_keyboard(lang, "missing data")
        await callback_query.message.edit_text(
            text=caption_err,
            reply_markup=keyboard_err,
        )

    caption, keyboard = re_get_marks_accepted_keyboard(lang, marks_state)

    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
    return


@re_require_auth
async def frontend_cb_re_eval_back_to_summary(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    await state.set_state(None)
    # When returning to summary, ensure chair edit mode is cleared if it was active
    await state.update_data(editing_target_access_key=None)
    await frontend_re_eval_finalize_score(callback_query, bot, state, db)


@re_require_auth
async def frontend_cb_re_chair_initiate_edit(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: Database
) -> None:
    """Handles a chairperson initiating an edit of another juror's scores."""
    lang = "ru" # Assuming lang, can be fetched or passed if needed
    
    data = await state.get_data()
    actor_is_chairman = data.get("is_chairman", False)

    if not actor_is_chairman:
        await callback_query.answer("Error: Only chairpersons can edit scores.", show_alert=True)
        return

    try:
        _, pres_id_str, target_juror_access_key = callback_query.data.split(":")
        pres_id = int(pres_id_str)
    except ValueError:
        await callback_query.answer("Error: Invalid callback data for edit.", show_alert=True)
        return

    # Set FSM state for chair editing mode
    await state.update_data(
        editing_target_access_key=target_juror_access_key,
        pres_id=str(pres_id) # Ensure pres_id is stored consistently (as string like other places)
    )

    # Navigate to the first criterion for editing
    # This assumes the evaluation flow starts with the first criterion in EVAL_CRITERIA
    first_criterion = EVAL_CRITERIA[0] if EVAL_CRITERIA else None
    if not first_criterion:
        # Handle error: No criteria defined
        caption_err, keyboard_err = re_get_error_keyboard(lang, "no criterion available")
        await callback_query.message.edit_text(text=caption_err, reply_markup=keyboard_err)
        return

    # Note: re_get_criterion_keyboard might need to be aware of the edit mode 
    # to potentially show existing scores of the target_juror for this pres_id and first_criterion.
    # For now, it will just show a blank scoring slate.
    caption, keyboard = re_get_criterion_keyboard(lang, str(pres_id), first_criterion)
    
    await callback_query.message.edit_text(
        text=caption,
        reply_markup=keyboard,
    )
