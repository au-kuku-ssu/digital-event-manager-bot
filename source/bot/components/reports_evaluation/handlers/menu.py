from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.reports_evaluation.handlers.keyboards import re_get_main_menu_keyboard
from components.reports_evaluation.fsm_states import REAuthStates

from components.shared.locale import get_locale_str, load_locales
from os.path import join, dirname

locale = load_locales(join(dirname(__file__), "..", "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

async def frontend_re_show_main_menu(message: types.Message, bot: Bot, state: FSMContext) -> None:
  """
  Handles showing main menu of reports evaluation.
  """
  lang = "ru"
  state_data = await state.get_data()
  jury_code = state_data.get("jury_code")
  jury_name = PLACEHOLDER_JURY[jury_code]["name"]

  keyboard = re_get_main_menu_keyboard(lang)
  await message.answer(
      getstr(lang, "reports_evaluation.menu.caption").format(jury_name=jury_name),
      reply_markup=keyboard
  )
