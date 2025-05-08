from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.reports_evaluation.utils import getstr


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
        text=getstr(lang, "reports_evaluation.menu.results"),
        callback_data="cb_re_results_page:0",
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.edit"), callback_data="cb_mm_main"
    )
    keyboard.button(
        text=getstr(lang, "reports_evaluation.menu.back_to_main_menu"),
        callback_data="cb_mm_main",
    )
    keyboard.adjust(1)

    return keyboard.as_markup()
