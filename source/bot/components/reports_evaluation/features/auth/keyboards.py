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


def re_get_auth_main_menu_keyboard(lang: str):
    """
    Creates and returns the caption and keyboard for returning to main menu.
    """
    caption = getstr(lang, "reports_evaluation.auth.too_many_attempts")

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.back_to_main_menu"),
        callback_data="cb_mm_main",
    )

    return caption, keyboard.as_markup()
