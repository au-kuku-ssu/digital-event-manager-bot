from aiogram.fsm.context import FSMContext
import logging

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.shared.db import Database # Import Database for type hinting and usage


async def re_submit_scores(
    state: FSMContext,
    db: Database,
    jury_id: int,
    participant_id: int,
    scores: dict,
):
    """
    Stores the submitted scores (already in DB) and optional comments into the database.
    Clears evaluation-specific data from FSM state.
    """
    data = await state.get_data()
    comments = data.get("pres_comments")

    if not all([participant_id, jury_id, scores is not None]):
        logging.error("Missing data for score submission (participant_id, jury_id, or scores)")
        return False

    cleaned_comments = ""
    if comments and comments.strip():
        cleaned_comments = comments.strip()
    
    # Update comment in the database
    try:
        await db.update_comment(jury_id, participant_id, cleaned_comments)
    except Exception as e:
        logging.error(f"Failed to update comment in DB: {e}")
        return False # Or handle error appropriately

    await state.update_data(pres_id=None, pres_comments=None, scores=None)

    return True


async def re_finalize_score(scores: dict):
    """
    Finalizes the score by summing up all the individual criteria scores.
    If a final_score already exists, it will not be overwritten.
    The final_score will not include the already calculated final score value, if present.
    """
    if not scores:
        logging.error("No scores provided to finalize.")
        return False

    # Check if all criteria are in the dict
    missing_criteria = [
        criteria for criteria in EVAL_CRITERIA if criteria not in scores
    ]
    if missing_criteria:
        logging.error(f"Missing scores for criteria: {', '.join(missing_criteria)}")
        return False

    total_score = sum(
        score for criteria, score in scores.items() if criteria in EVAL_CRITERIA
    )
    scores["final_score"] = total_score
    return True
