from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.utils import getstr


def re_get_auth_continue_keyboard(lang: str):
    """
    Creates and returns the caption and the keyboard with a continue button to the main menu.
    """
    caption = getstr(lang, "reports_evaluation.auth.continue_caption")
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.auth.continue"),
        callback_data="cb_re_main_menu",
    )

    return caption, keyboard.as_markup()
