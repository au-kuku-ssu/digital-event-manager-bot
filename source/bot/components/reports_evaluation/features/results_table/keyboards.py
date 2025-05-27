from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.utils import getstr


def re_get_results_table_keyboard(
    lang: str,
    presentations_from_db: list[dict],
    page: int = 0,
    per_page: int = 5,
    is_chairman: bool = False,
):
    """
    Returns a caption with the results table and navigation keyboard.
    Displays speakers, topic, individual jury scores (or "-"), and comments from DB data.
    If is_chairman is True, adds edit buttons for each juror's scores.
    """

    def format_presentation(pres: dict, idx: int) -> str:
        speakers = ", ".join(pres.get("speakers", ["N/A"]))
        topic = pres.get("topic", "N/A")
        final_score_display = pres.get("final_score", "-")
        presentation_id = pres.get("id")

        table_lines = []
        comment_lines = []
        edit_buttons_for_chairman = InlineKeyboardBuilder()

        for evaluation in pres.get("jury_evaluations", []):
            juror_name = evaluation.get("juror_name", "Unknown Juror")
            juror_access_key = evaluation.get("juror_access_key")
            juror_scores = evaluation.get("scores", {})
            juror_comment = evaluation.get("comment", "")
            juror_specific_final_score = evaluation.get("juror_final_score", "-")

            score_values = [
                str(juror_scores.get(criterion, "-")).rjust(3) for criterion in EVAL_CRITERIA
            ]
            score_values.append(str(juror_specific_final_score).rjust(3))

            line = f"{juror_name:<25} | " + " ".join(score_values)
            if is_chairman and juror_access_key and presentation_id:
                edit_button_text = f"Edit {juror_name.split()[0]}'s scores"
                edit_callback_data = f"cb_re_chair_edit_init:{presentation_id}:{juror_access_key}"
                line += f" (✏️)"

            table_lines.append(line)

            if juror_comment and juror_comment.strip():
                comment_lines.append(f"💬 <i>{juror_name}</i>: {juror_comment.strip()}")

        if is_chairman and presentation_id:
            for evaluation in pres.get("jury_evaluations", []):
                juror_name = evaluation.get("juror_name", "Unknown Juror")
                juror_access_key = evaluation.get("juror_access_key")
                if juror_access_key:
                    edit_buttons_for_chairman.button(
                        text=f"Edit {juror_name}",
                        callback_data=f"cb_re_chair_edit_init:{presentation_id}:{juror_access_key}"
                    )
            if pres.get("jury_evaluations"):
                edit_buttons_for_chairman.adjust(1)

        criteria_header_short = " ".join([crit[:3].upper() for crit in EVAL_CRITERIA]) + " FIN"
        header_line = f"{'Jury Member':<25} | {criteria_header_short}"
        if not pres.get("jury_evaluations", []):
            table_lines.append(f"{'No scores submitted yet.':<25}")

        formatted_text = (
            f"<b>#{idx}</b> | {speakers}\n"
            f"<b>{topic}</b>\n"
            f"<b>{getstr(lang, 'reports_evaluation.results_table.final_score')}:</b> {final_score_display}\n"
            f"<pre>{header_line}\n"
            + "\n".join(table_lines)
            + "</pre>\n"
            + ("\n".join(comment_lines) if comment_lines else "")
        ).strip()

        return formatted_text, edit_buttons_for_chairman

    def sort_key(p):
        fs = p.get("final_score")
        if isinstance(fs, (int, float)):
            return -fs
        return float("inf")

    sorted_presentations = sorted(presentations_from_db, key=sort_key)

    total_pages = (len(sorted_presentations) - 1) // per_page + 1
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = start + per_page
    current_presentations_on_page = sorted_presentations[start:end]

    caption_parts = [
        f"<b>{getstr(lang, 'reports_evaluation.results_table.caption')}</b>\n\n",
        f"<i>{getstr(lang, 'reports_evaluation.results_table.header_hint')}</i>\n\n"
    ]
    
    if not current_presentations_on_page:
        caption_parts.append(getstr(lang, "reports_evaluation.results_table.empty"))
    else:
        overall_keyboard_builder = InlineKeyboardBuilder()
        for i, p_data in enumerate(current_presentations_on_page, start=start):
            presentation_text, presentation_edit_buttons_builder = format_presentation(p_data, i + 1)
            caption_parts.append(presentation_text)
            for row in presentation_edit_buttons_builder.export():
                overall_keyboard_builder.row(*row)            
            caption_parts.append("\n")

    caption = "\n".join(caption_parts).strip()

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
        overall_keyboard_builder.row(*nav_buttons)

    overall_keyboard_builder.row(
        types.InlineKeyboardButton(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_re_main_menu",
        )
    )

    return caption, overall_keyboard_builder.as_markup()
