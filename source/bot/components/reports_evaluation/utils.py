from functools import wraps
from os.path import join, dirname

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from components.main_menu.frontend import frontend_cb_mm_main
from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))


def getstr(lang: str, path: str) -> str:
    """
    Returns string from locale.
    """
    return get_locale_str(locale, f"{lang}.{path}")


async def re_check_access_code(code: str):
    """
    Checks if access code is valid.
    """
    jury_data = PLACEHOLDER_JURY

    for juror in jury_data:
        if juror == code:
            return juror

    return None


def re_require_auth(handler):
    """
    Ensures that the user is authenticated. If not, returns the user to the main menu (cb_mm_main).
    """

    @wraps(handler)
    async def wrapper(
        callback_query: types.CallbackQuery,
        bot: Bot,
        state: FSMContext,
        *args,
        **kwargs,
    ):
        state_data = await state.get_data()

        if "auth_code" not in state_data:
            # TODO: Lang instead of just text
            await callback_query.answer(
                text="Authentication failed.",
                reply_markup=types.ReplyKeyboardRemove(),
                show_alert=True,
            )
            await frontend_cb_mm_main(callback_query, bot)
            return None

        return await handler(callback_query, bot, state, *args, **kwargs)

    return wrapper


async def re_add_auth_message(state: FSMContext, message_id: int):
    """
    Adds auth messages (both user's and bot's) into a state value.
    """
    state_data = await state.get_data()
    msg_ids = list(state_data.get("re_auth_message_ids", []))
    msg_ids.append(message_id)
    await state.update_data(re_auth_message_ids=msg_ids)


async def re_delete_auth_messages(state: FSMContext, chat_id: int, bot: Bot):
    """
    Deletes auth messages (both user's and bot's) from chat history.
    """
    # TODO: May not handle race condition
    state_data = await state.get_data()
    msg_ids = state_data.get("re_auth_message_ids", [])

    if msg_ids:
        for msg_id in msg_ids:
            try:
                await bot.delete_message(chat_id, msg_id)
            except TelegramBadRequest:
                pass

        await state.update_data(re_auth_message_ids=None)
