from aiogram import types


from components.reports_evaluation.data.criterion_data import EVAL_CRITERIA

from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.utils import getstr


def re_get_presentations_keyboard(
    lang: str,
    presentations: list,
    juror_code: str,
    page: int = 0,
    per_page: int = 5,
    edit: bool = False,
):
    """
    Creates and returns the keyboard for presentations with navigation options.
    Displays only those presentations which haven't been rated by the reviewer (juror_code).

    If in edit mode, shows all presentations.
    """
    # Filter presentations only if not editing
    filtered_presentations = (
        [pres for pres in presentations if juror_code not in pres["jury_scores"]]
        if not edit
        else presentations
    )

    # Return if none
    if len(filtered_presentations) == 0:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_re_main_menu",
        )
        keyboard.adjust(1)
        return None, keyboard.as_markup()

    keyboard = InlineKeyboardBuilder()
    total_pages = (len(filtered_presentations) - 1) // per_page + 1
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = start + per_page
    current_presentations = filtered_presentations[start:end]

    caption_lines = []
    caption = f"{getstr(lang, 'reports_evaluation.presents.caption')}\n\n"

    # Cycling through presentations and displaying 'per_page' of them as captions and buttons
    for idx, pres in enumerate(current_presentations, start=1 + start):
        short_abstract = (
            (pres["abstract"][:150] + "...")
            if len(pres["abstract"]) > 150
            else pres["abstract"]
        )
        line = (
            f"#️⃣ <b>{idx}</b>\n"
            f"{getstr(lang, 'reports_evaluation.presents.theme')} {pres['topic']}\n"
            f"{getstr(lang, 'reports_evaluation.presents.speakers')} {', '.join(pres['speakers'])}\n"
            f"{getstr(lang, 'reports_evaluation.presents.description')} {short_abstract}"
        )
        caption_lines.append(line)

        keyboard.button(text=f"{idx}", callback_data=f"cb_re_choose_pres:{pres['id']}")

    caption += "\n\n".join(caption_lines)

    # Creating nav_buttons, if necessary
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text=getstr(lang, "reports_evaluation.presents.back"),
                callback_data=f"cb_re_pres_page:{page - 1}"
                if not edit
                else f"cb_re_edit_pres_page:{page - 1}",
            )
        )
    if end < len(filtered_presentations):
        nav_buttons.append(
            types.InlineKeyboardButton(
                text=getstr(lang, "reports_evaluation.presents.forward"),
                callback_data=f"cb_re_pres_page:{page + 1}"
                if not edit
                else f"cb_re_edit_pres_page:{page + 1}",
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


def re_get_criterion_keyboard(lang: str, criterion: str, score_range: int = 5):
    """
    Creates and returns the keyboard for a specific evaluation criterion.
    Includes score buttons from 0 to score_range - 1, and navigation buttons:
    - 'Return' to the previous criterion (if available)
    - 'Back' to return to the main menu
    """
    caption = getstr(lang, f"reports_evaluation.evaluation.{criterion}")
    keyboard = InlineKeyboardBuilder()

    # Build score buttons
    for i in range(score_range):
        keyboard.button(
            text=str(i),
            callback_data=f"cb_re_score:{criterion}:{i}",
        )
    keyboard.adjust(score_range)

    # Nav buttons
    nav_buttons = []
    # Check if you can come back to previous notes
    if criterion in EVAL_CRITERIA:
        idx = EVAL_CRITERIA.index(criterion)
        if idx > 0:
            previous_criterion = EVAL_CRITERIA[idx - 1]
            nav_buttons.append(
                types.InlineKeyboardButton(
                    text=getstr(lang, "reports_evaluation.evaluation.return"),
                    callback_data=f"cb_re_return_to_score:{previous_criterion}",
                )
            )
    # Return to the main menu button
    nav_buttons.append(
        types.InlineKeyboardButton(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_re_main_menu",
        )
    )
    keyboard.row(*nav_buttons)

    return caption, keyboard.as_markup()


def re_get_final_score_keyboard(lang: str, scores: dict[str, int], pres_id: str):
    """
    Builds and returns the final confirmation keyboard after all criteria are scored.
    Displays a summary of all criterion scores and offers 'Accept' or 'Decline' options.
    """
    caption = getstr(lang, "reports_evaluation.evaluation.final_score") + "\n"

    lines = [
        f"<b>{criterion.capitalize()}:</b> {scores.get(criterion, '-')}"
        for criterion in scores
    ]
    caption += "\n".join(lines)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.accept"),
        callback_data="cb_re_eval_comment",
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.decline"),
        callback_data=f"cb_re_choose_pres:{pres_id}",
    )
    keyboard.adjust(1)

    return caption, keyboard.as_markup()


def re_get_comment_keyboard(lang: str):
    """
    Generates the keyboard for the optional commentary step.
    Includes a button to skip writing comments and proceed with submission.
    """
    caption = getstr(lang, "reports_evaluation.evaluation.comment")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.skip_comments"),
        callback_data="cb_re_eval_marks_accepted",
    )
    keyboard.adjust(1)

    return caption, keyboard.as_markup()


def re_get_marks_accepted_keyboard(lang: str, marks_state: bool):
    """
    Generates caption and keyboard to continue to main menu after skipping comments.
    """
    caption = getstr(
        lang,
        "reports_evaluation.evaluation.marks_accepted"
        if marks_state
        else "reports_evaluation.evaluation.marks_declined",
    )

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.marks_continue"),
        callback_data="cb_re_main_menu",
    )

    return caption, keyboard.as_markup()


def re_get_comment_check_keyboard(lang: str, comment: str):
    caption = getstr(lang, "reports_evaluation.evaluation.comment_check_caption")

    caption += "\n" + getstr(
        lang, "reports_evaluation.evaluation.comment_check_comment"
    ).format(comment=comment)

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.comment_check_edit"),
        callback_data="cb_re_eval_comment",
    )

    keyboard.button(
        text=getstr(lang, "reports_evaluation.evaluation.comment_check_continue"),
        callback_data="cb_re_eval_marks_accepted",
    )
    keyboard.adjust(1)

    return caption, keyboard.as_markup()
