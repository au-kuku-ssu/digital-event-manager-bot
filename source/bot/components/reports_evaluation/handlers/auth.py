from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from components.reports_evaluation.fsm_states import REAuthStates
from components.reports_evaluation.handlers.menu import frontend_re_show_main_menu
from components.reports_evaluation.handlers.keyboards import re_get_back_keyboard
from components.reports_evaluation.utils import re_check_access_code
from components.shared.locale import get_locale_str, load_locales
from os.path import join, dirname

locale = load_locales(join(dirname(__file__), "..", "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

async def frontend_cb_re_auth(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
  """
  Shows user prompt for entering access code.
  """
  await state.clear()
  lang = "ru"

  await state.set_state(REAuthStates.waiting_for_code)
  await callback_query.message.edit_text(
    getstr(lang, "reports_evaluation.auth.caption")
  )

async def frontend_st_re_process_code(message: types.Message, bot: Bot, state: FSMContext) -> None:
  """
  Handles juror authorization based on input code.
  - On success: stores code, sets state, shows main menu.
  - On failure: shows error message with a back button.
  """
  lang = "ru"
  code = message.text.strip()

  juror = re_check_access_code(code)

  if juror:
    await state.update_data(jury_code=code)
    await state.set_state(REAuthStates.authorized)
    await frontend_re_show_main_menu(message, bot, state)
  else:
    await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"))

    # Code below spams a lot of windows, so the "back" button is turned off.
    # keyboard = re_get_back_keyboard(lang)
    # await message.answer(getstr(lang, "reports_evaluation.auth.invalid_code"), reply_markup=keyboard)

