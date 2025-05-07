# TODO: Change placeholders to db change
from aiogram.fsm.context import FSMContext

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
            print(f"[DEBUG] Updated presentation: {pres}")
            break
    else:
        print(f"[ERROR] Presentation {pres_id} not found")
        return False

    await state.update_data(scores=None, pres_id=None, pres_comments=None)

    return True
