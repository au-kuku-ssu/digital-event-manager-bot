# TODO: Change placeholders to db change
from aiogram.fsm.context import FSMContext

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.data.placeholder_presentations import (
    PLACEHOLDER_PRESENTS,
)


async def re_submit_scores(state: FSMContext):
    """
    Stores the submitted scores and optional comments into the PLACEHOLDER_PRESENTS data structure.
    Finds the presentation by ID and attaches the scores by juror ID.
    """
    data = await state.get_data()
    scores = data.get("scores", {})
    pres_id = data.get("pres_id")
    juror_id = data.get("jury_code")
    comments = data.get("pres_comments")

    if not all([pres_id, juror_id, scores]):
        print("[ERROR] Missing data in state")
        # print(f"[DEBUG] {scores}, {pres_id}, {juror_id}")
        return False

    # Убедимся, что комментарий очищен, если он пустой
    cleaned_comments = comments.strip() if comments and comments.strip() else ""

    # Set scores
    for pres in PLACEHOLDER_PRESENTS:
        if pres["id"] == pres_id:
            pres["jury_scores"][juror_id] = scores
            pres["comments"][juror_id] = cleaned_comments

            # Update final score
            total_final_scores = 0
            final_score = 0
            num_jurors = len(pres["jury_scores"])

            # Safe access to juror_score
            for juror_score in pres["jury_scores"].values():
                total_final_scores += juror_score.get("final_score", 0)

            if num_jurors > 0:
                final_score = total_final_scores / num_jurors

            pres["final_score"] = final_score

            # print(f"[DEBUG] Updated presentation: {pres}")
            break
    else:
        print(f"[ERROR] Presentation {pres_id} not found")
        return False

    await state.update_data(scores=None, pres_id=None, pres_comments=None)

    return True


async def re_finalize_score(state: FSMContext):
    """
    Finalizes the score by summing up all the individual criteria scores.
    If a final_score already exists, it will not be overwritten.
    The final_score will not include the already calculated final score value, if present.
    """
    state_data = await state.get_data()
    scores = dict(state_data.get("scores", {}))

    # Check if all criteria are in the dict
    missing_criteria = [
        criteria for criteria in EVAL_CRITERIA if criteria not in scores
    ]
    if missing_criteria:
        print(f"[ERROR] Missing scores for criteria: {', '.join(missing_criteria)}")
        return

    total_score = sum(
        score for criteria, score in scores.items() if criteria in EVAL_CRITERIA
    )
    scores["final_score"] = total_score
    await state.update_data(scores=scores)
    # print(f"[INFO] Final score calculated and updated: {total_score}")
