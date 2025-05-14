from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.utils import getstr


def re_get_edit_results_keyboard(lang: str, jury: dict):
    """
    Generates a keyboard for the chairman to select a jury member for result editing.

    If the user is confirmed to be a chairman, a button for each jury member (with their name)
    is added to the keyboard. Each button leads to selection of a specific jury via callback.
    Also includes a 'Back to main menu' button. If not a chairman, returns a restricted access caption.
    """
    # TODO: Instead of jury_code hashed version should be used
    caption = getstr(lang, "reports_evaluation.edit_results.caption")

    keyboard = InlineKeyboardBuilder()

    for jury_code, jury_info in jury.items():
        name = jury_info.get("name", "Unnamed")
        callback_data = f"cb_re_edit_select_jury:{jury_code}"
        keyboard.button(text=name, callback_data=callback_data)
    keyboard.adjust(1)

    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.back"),
        callback_data="cb_re_main_menu",
    )
    keyboard.adjust(1)

    return caption, keyboard.as_markup()


def re_get_select_jury_keyboard(lang: str, wrong_code: bool):
    """
    Generates a confirmation or error keyboard after a jury member is selected.

    Displays a confirmation message and a 'Continue' button if the selected jury_code is valid.
    If the code is invalid, shows an error message and a button to return to the main menu.
    """
    caption = (
        getstr(lang, "reports_evaluation.edit_results.jury_selected")
        if not wrong_code
        else getstr(lang, "reports_evaluation.edit_results.error")
    )

    keyboard = InlineKeyboardBuilder()

    if wrong_code:
        keyboard.button(
            text=getstr(lang, "reports_evaluation.menu.back"),
            callback_data="cb_re_main_menu",
        )
    else:
        keyboard.button(
            text=getstr(lang, "reports_evaluation.edit_results.continue"),
            callback_data="cb_re_edit_pres_page:0",
        )

    return caption, keyboard.as_markup()
