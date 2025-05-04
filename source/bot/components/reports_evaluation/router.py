from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from components.reports_evaluation.frontend import frontend_cb_re_auth, frontend_st_re_process_code
from components.reports_evaluation.fsm_states import REAuthStates

router = Router()

# Authorization
@router.callback_query(lambda c: c.data == "cb_re_main")
async def cb_re_main_menu(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
  await frontend_cb_re_auth(callback_query, bot, state)

@router.message(REAuthStates.waiting_for_code)
async def st_re_process_code(message: types.Message, bot: Bot, state: FSMContext) -> None:
  await frontend_st_re_process_code(message, bot, state)
