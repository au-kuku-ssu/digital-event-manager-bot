from aiogram.utils.keyboard import InlineKeyboardBuilder
from components.shared.locale import get_locale_str, load_locales
from os.path import join, dirname

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

def re_get_back_keyboard(lang: str):
  keyboard = InlineKeyboardBuilder()

  keyboard.button(text=getstr(lang, "reports_evaluation.menu.back"), callback_data="cb_mm_main")
  keyboard.adjust(1)

  return keyboard.as_markup()

def re_get_main_menu_keyboard(lang: str):
  keyboard = InlineKeyboardBuilder()

  keyboard.button(text=getstr(lang, "reports_evaluation.menu.evaluate"), callback_data="cb_mm_main")
  keyboard.button(text=getstr(lang, "reports_evaluation.menu.results"), callback_data="cb_mm_main")
  keyboard.button(text=getstr(lang, "reports_evaluation.menu.edit"), callback_data="cb_mm_main")
  keyboard.button(text=getstr(lang, "reports_evaluation.menu.back"), callback_data="cb_mm_main")
  keyboard.adjust(1)

  return keyboard.as_markup()
