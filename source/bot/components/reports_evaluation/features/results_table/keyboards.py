from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA
from components.reports_evaluation.utils import getstr


def re_get_results_table_keyboard(
    lang: str,
    presentations: list[dict],
    juries: list[tuple[str, str, str]],
    page: int = 0,
    per_page: int = 5,
):
    """
    Returns a caption with the results table and navigation keyboard.
    Displays speakers, topic, individual jury scores (or "-"), and comments.
    """

    # TODO: More like a template. Should be remade when db will be in use.
    def format_presentation(pres: dict, idx: int) -> str:
        speakers = ", ".join(pres["speakers"])
        topic = pres["topic"]
        final_score = pres.get("final_score", "-")

        # Prepare aligned table of jury scores
        jury_scores = pres.get("jury_scores", {})
        comment_lines = []

        table_lines = []
        for jury in juries:
            name = f"{jury[1]} {jury[2]}"
            scores = jury_scores.get(jury[0], {})
            score_values = [
                str(scores.get(criterion, "-")).rjust(3) for criterion in EVAL_CRITERIA
            ]
            score_values.append(str(scores.get("final_score", "-")).rjust(3))

            line = f"{name:<25} | " + " ".join(score_values)
            table_lines.append(line)

        # Collect comments
        for jury in juries:
            comment = pres.get("comments", {}).get(jury[0], "")
            if comment and comment.strip():
                jury_name = f"{jury[1]} {jury[2]}"
                comment_lines.append(f"💬 <i>{jury_name}</i>: {comment.strip()}")

        return (
            f"<b>#{idx}</b> | {speakers}\n"
            f"<b>{topic}</b>\n"
            f"<b>{getstr(lang, 'reports_evaluation.results_table.final_score')}:</b> {final_score}\n"
            f"<pre>{'Jury Member':<25} | Org Con Vis Mec Del Fin\n"
            + "\n".join(table_lines)
            + "</pre>\n"
            + ("\n".join(comment_lines) if comment_lines else "")
        ).strip()

    # Sort by final_score descending (or push empty to the end)
    def sort_key(p):
        try:
            return -float(p.get("final_score", ""))
        except (ValueError, TypeError):
            return float("inf")

    sorted_presentations = sorted(presentations, key=sort_key)

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
