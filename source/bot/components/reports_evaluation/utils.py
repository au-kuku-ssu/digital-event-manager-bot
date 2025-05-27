import logging  # Added
from functools import wraps
from os.path import join, dirname
from typing import Optional  # Added

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from components.shared.locale import load_locales, get_locale_str
from components.shared.db import Database

logger = logging.getLogger(__name__)

locale = load_locales(join(dirname(__file__), "locale"))


def getstr(lang: str, path: str) -> str:
    """
    Returns string from locale.
    """
    return get_locale_str(locale, f"{lang}.{path}")


async def re_check_access_code(db: Database, code: str) -> Optional[bool]:
    """
    Checks access code and returns jury role (is_chairman as bool) by calling a method on the Database object.
    Runs synchronous DB operations in a thread pool.
    """
    try:
        return await db.get_jury_role_by_access_key(code)
    except Exception as e:
        logger.error(f"Error calling db.get_jury_role_by_access_key: {e}")
        return None


def re_require_auth(handler):
    """
    Ensures that the user is authenticated. If not, returns the user to the main menu (cb_mm_main)
    or denies access. It also validates the auth_code from state against the database and stores the role.
    """

    @wraps(handler)
    async def wrapper(
        event: types.TelegramObject,  # Changed to TelegramObject to handle both Message and CallbackQuery
        bot: Bot,
        state: FSMContext,
        db: Database,  # Expect db to be passed by the middleware via dispatcher
        *args,
        **kwargs,
    ):
        state_data = await state.get_data()
        auth_code = state_data.get("auth_code")

        # Determine how to respond based on event type
        async def answer_auth_failed(text="Authentication failed."):
            if isinstance(event, types.CallbackQuery):
                await event.answer(text=text, show_alert=True)
                # Potentially redirect to main menu, e.g., by editing message
                # await frontend_cb_mm_main(event, bot) # Ensure frontend_cb_mm_main can handle this
            elif isinstance(event, types.Message):
                await event.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
            # For other event types, this might need adjustment

        if not auth_code:
            logger.warning(
                f"Auth attempt failed: no auth_code in state for user {event.from_user.id if event.from_user else 'Unknown'}."
            )
            await answer_auth_failed()
            # If it's a callback query, we might want to call frontend_cb_mm_main
            # This depends on whether frontend_cb_mm_main is designed to be called from here
            # and if it correctly handles the UI flow.
            if isinstance(event, types.CallbackQuery):
                # Example: await frontend_cb_mm_main(event, bot, state) # Pass state if needed
                pass  # Placeholder for actual redirection logic
            return None

        if (
            not db or not db.cursor
        ):  # Also check if cursor is available as db operations need it
            logger.error(
                "Database instance or cursor not available in re_require_auth."
            )
            await answer_auth_failed("System error: Cannot verify access.")
            return None

        is_chairman_role = await re_check_access_code(db, auth_code)
        if (
            is_chairman_role is None
        ):  # Check if role is None (meaning key not found or error)
            logger.warning(
                f"Auth attempt failed: invalid access code '{auth_code}' for user {event.from_user.id if event.from_user else 'Unknown'}."
            )
            await answer_auth_failed("Invalid access code.")
            # Similar to above, handle redirection if necessary
            if isinstance(event, types.CallbackQuery):
                # await frontend_cb_mm_main(event, bot, state)
                pass
            return None

        # Store the fetched jury_role in the state
        await state.update_data(is_chairman=is_chairman_role)
        logger.info(
            f"User {event.from_user.id if event.from_user else 'Unknown'} authenticated successfully. Is chairman: {is_chairman_role}"
        )

        # If all checks pass, proceed with the original handler
        # Pass db explicitly if the handler expects it as a named argument
        # or ensure it's in kwargs if the handler pulls it from there.
        # The middleware already adds 'db' to the data dict, so handlers
        # configured to receive it via **kwargs or data['db'] should work.
        return await handler(event, bot, state, db=db, *args, **kwargs)  # Pass db along

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
