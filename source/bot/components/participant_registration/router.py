from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext


from source.bot.components.participant_registration.logic.states import RegisterStates
from source.bot.components.participant_registration.logic.main import pr_cb_main
from source.bot.components.participant_registration.logic.browse import (
    pr_cb_user_browse,
)
from source.bot.components.participant_registration.logic.register import (
    pr_cb_user_register,
    pr_cb_reg_lst_frm_section,
    pr_cb_reg_prt_frm_section,
)

from source.bot.components.participant_registration.logic.my_data import (
    pr_cb_user_my_data,
    pr_cb_add_user_fio,
    pr_cb_add_user_phone,
    pr_cb_handle_fio_input,
    pr_cb_handle_email_input,
    pr_cb_handle_phone_input,
)


router = Router()


@router.callback_query(lambda c: c.data == "pr_cb_main")
async def callback_user_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_main(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_user_browse")
async def callback_user_events_browse(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_browse(callback_query, bot, state)


# ---------------------------- My_data routers -----------------------------------------


@router.callback_query(lambda c: c.data == "pr_cb_user_my_data")
async def callback_user_my_data(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_my_data(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_add_user_fio")
async def callback_add_user_fio(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_add_user_fio(callback_query, bot, state)


@router.message(RegisterStates.fio)
async def msg_fio(message: types.Message, state: FSMContext):
    await pr_cb_handle_fio_input(message, state)


@router.callback_query(lambda c: c.data == "pr_cb_add_user_phone")
async def callback_add_user_phone(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_add_user_phone(callback_query, bot, state)


@router.message(RegisterStates.phone)
async def msg_phone(message: types.Message, state: FSMContext):
    await pr_cb_handle_phone_input(message, state)


@router.message(RegisterStates.email)
async def msg_email(message: types.Message, state: FSMContext):
    await pr_cb_handle_email_input(message, state)


# ---------------------------- Registration routers -----------------------------------------


@router.callback_query(lambda c: c.data == "pr_cb_user_register")
async def callback_user_register(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_register(callback_query, bot, state)


# Listener ---------------------------------------------------------------------
@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_section")
async def callback_reg_listener_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_section(callback_query, bot, state)


# Participant ---------------------------------------------------------------------
@router.callback_query(lambda c: c.data == "pr_cb_reg_prt_frm_section")
async def callback_reg_participant_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_prt_frm_section(callback_query, bot, state)
