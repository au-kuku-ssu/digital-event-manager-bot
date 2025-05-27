from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.utils import getstr


def re_get_results_table_keyboard(
    lang: str,
    presentations_from_db: list[dict],
    page: int = 0,
    per_page: int = 5,
):
    """
    Returns a caption with the results table and navigation keyboard.
    Displays speakers, topic, individual jury scores (or "-"), and comments from DB data.
    """

    def format_presentation(pres: dict, idx: int) -> str:
        speakers = ", ".join(pres.get("speakers", ["N/A"]))
        topic = pres.get("topic", "N/A")
        # Overall final_score for the presentation, calculated in the DB method
        final_score_display = pres.get("final_score", "-")

        table_lines = []
        comment_lines = []
        unique_jurors_for_header = [] # To build the header dynamically if needed, or use a fixed list

        # pres["jury_evaluations"] contains all evaluations for this presentation
        for evaluation in pres.get("jury_evaluations", []):
            juror_name = evaluation.get("juror_name", "Unknown Juror")
            # juror_access_key = evaluation.get("juror_access_key") # Available if needed
            juror_scores = evaluation.get("scores", {}) # Dict of criteria:score
            juror_comment = evaluation.get("comment", "")
            # juror_specific_final_score = evaluation.get("juror_final_score", "-") # Final score by this juror

            # Prepare score values for table line
            score_values = [
                str(juror_scores.get(criterion, "-")).rjust(3) for criterion in EVAL_CRITERIA
            ]
            # Add the juror's own total for this presentation
            score_values.append(str(evaluation.get("juror_final_score", "-")).rjust(3))

            line = f"{juror_name:<25} | " + " ".join(score_values)
            table_lines.append(line)

            if juror_comment and juror_comment.strip():
                comment_lines.append(f"💬 <i>{juror_name}</i>: {juror_comment.strip()}")

            if juror_name not in unique_jurors_for_header:
                unique_jurors_for_header.append(juror_name)

        # Header for the score table - uses EVAL_CRITERIA + a "Fin" for juror's total
        criteria_header_short = " ".join([crit[:3].upper() for crit in EVAL_CRITERIA]) + " FIN"
        header_line = f"{'Jury Member':<25} | {criteria_header_short}"
        # Fallback if no evaluations for this presentation
        if not table_lines:
            table_lines.append(f"{'No scores submitted yet.':<25}")

        return (
            f"<b>#{idx}</b> | {speakers}\n"
            f"<b>{topic}</b>\n"
            f"<b>{getstr(lang, 'reports_evaluation.results_table.final_score')}:</b> {final_score_display}\n"
            f"<pre>{header_line}\n"
            + "\n".join(table_lines)
            + "</pre>\n"
            + ("\n".join(comment_lines) if comment_lines else "")
        ).strip()

    # Sort by final_score descending (or push empty/non-numeric to the end)
    def sort_key(p):
        fs = p.get("final_score")
        if isinstance(fs, (int, float)):
            return -fs
        return float("inf") # Non-numeric or missing scores go to the end

    sorted_presentations = sorted(presentations_from_db, key=sort_key)

    total_pages = (len(sorted_presentations) - 1) // per_page + 1
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = start + per_page
    current_presentations = sorted_presentations[start:end]

    caption_lines = [
        format_presentation(p, idx + 1)
        for idx, p in enumerate(current_presentations, start=start)
    ]

    caption = (
        f"<b>{getstr(lang, 'reports_evaluation.results_table.caption')}</b>\n\n"
        f"<i>{getstr(lang, 'reports_evaluation.results_table.header_hint')}</i>\n\n"
        + "\n\n".join(caption_lines)
        or getstr(lang, "reports_evaluation.results_table.empty")
    )

    keyboard = InlineKeyboardBuilder()
    nav_buttons = []

    if page > 0:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text=getstr(lang, "reports_evaluation.results_table.back"),
                callback_data=f"cb_re_results_page:{page - 1}",
            )
        )
    if end < len(sorted_presentations):
        nav_buttons.append(
            types.InlineKeyboardButton(
                text=getstr(lang, "reports_evaluation.results_table.forward"),
                callback_data=f"cb_re_results_page:{page + 1}",
            )
        )
    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.row(
        types.InlineKeyboardButton(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_re_main_menu",
        )
    )

    return caption, keyboard.as_markup()
