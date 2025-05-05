from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from components.shared.locale import get_locale_str, load_locales
from os.path import join, dirname

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")


def re_get_back_keyboard(lang: str):
    """
    Creates and returns the keyboard with a back button to the main menu.
    """
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.back"), callback_data="cb_mm_main"
    )
    keyboard.adjust(1)

    return keyboard.as_markup()


def re_get_main_menu_keyboard(lang: str):
    """
    Creates and returns the main menu keyboard for reports evaluation.
    Provides options for evaluating, viewing results, editing, or going back to the main menu.
    """
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.evaluate"),
        callback_data="cb_re_pres_page:0",
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.results"), callback_data="cb_mm_main"
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.edit"), callback_data="cb_mm_main"
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.back"), callback_data="cb_mm_main"
    )
    keyboard.adjust(1)

    return keyboard.as_markup()


def re_get_presentations_keyboard(
    lang: str, presentations: list, page: int = 0, per_page: int = 5
):
    """
    Creates and returns the keyboard for presentations with navigation options.
    Displays up to 5 presentations per page, with options to navigate between pages and select a presentation.
    """
    keyboard = InlineKeyboardBuilder()
    total_pages = (len(presentations) - 1) // per_page + 1
    page = max(0, min(page, total_pages - 1))

    start = page * per_page
    end = start + per_page
    current_presentations = presentations[start:end]

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
                callback_data=f"cb_re_pres_page:{page - 1}",
            )
        )
    if end < len(presentations):
        nav_buttons.append(
            types.InlineKeyboardButton(
                text=getstr(lang, "reports_evaluation.presents.forward"),
                callback_data=f"cb_re_pres_page:{page + 1}",
            )
        )

    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.row(
        types.InlineKeyboardButton(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_mm_main",
        )
    )

    return caption, keyboard.as_markup()
