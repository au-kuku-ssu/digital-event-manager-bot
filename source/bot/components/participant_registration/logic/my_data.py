import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str
from components.participant_registration.logic.states import RegisterStates

from database.db import (
    register_user_from_state,
    get_user_by_tg_name,
    get_user_by_email,
    update_user_from_state,
)

import re

locale = load_locales(join(dirname(__file__), "..", "locale"))

prefix = "participant_registration.user.my_data"
shared = "participant_registration.shared"

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
VERIFICATION_CODES = {}
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("TG_BOT_EMAIL_PASSWORD")
EMAIL_FROM = os.environ.get("TG_BOT_EMAIL")


def getstr(lang, prefix, path):
    return get_locale_str(locale, f"{lang}.{prefix}.{path}")


async def pr_cb_user_my_data(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    keyboard = InlineKeyboardBuilder()

    tg_name = callback_query.from_user.username or f"id{callback_query.from_user.id}"

    user_data = get_user_by_tg_name(tg_name)

    if user_data:
        keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

        keyboard.button(
            text=getstr(lang, prefix, "change_info"),
            callback_data="pr_cb_change_user_fio",
        )

        await callback_query.message.edit_text(
            text=f"{getstr(lang, prefix, 'show_info.fio')}: {user_data.get('last_name', '')} "
                 f"{user_data.get('first_name', '')} {user_data.get('middle_name', '')}\n"
                 f"{getstr(lang, prefix, 'show_info.phone')}: {user_data.get('phone', '')}\n"
                 f"{getstr(lang, prefix, 'show_info.email')}: {user_data.get('email', '')}",
            reply_markup=keyboard.as_markup(),
        )
    else:
        keyboard.button(
            text=getstr(lang, prefix, "add_user"), callback_data="pr_cb_add_user_fio"
        )
        keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

        await callback_query.message.edit_text(
            text=getstr(lang, prefix, "error.no_user.caption"),
            reply_markup=keyboard.as_markup(),
        )


# Add user ---------------------------------------------------------------------------------


async def pr_cb_add_user_fio(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await callback_query.message.edit_text(text=getstr(lang, prefix, "fio"))
    await state.set_state(RegisterStates.fio)


async def pr_cb_handle_fio_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.update_data(fio=message.text.strip())
    await message.answer(text=getstr(lang, prefix, "phone"))
    await state.set_state(RegisterStates.phone)


async def pr_cb_add_user_phone(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await callback_query.message.edit_text(text=getstr(lang, prefix, "phone"))
    await state.set_state(RegisterStates.phone)


async def pr_cb_handle_phone_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    phone_number = message.text.strip()
    if not validate_phone(phone_number):
        await message.answer(text=getstr(lang, prefix, "error.wrong_phone.caption"))
        return

    await state.update_data(phone=phone_number)
    await message.answer(text=getstr(lang, prefix, "email"))
    await state.set_state(RegisterStates.email)


def validate_phone(phone_number):
    """
    Checks the format of the phone number (Russian numbers)
    Acceptable formats:
    +7XXX..., 8XXX..., 7XXX...
    """
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return re.match(pattern, phone_number) is not None


async def pr_cb_handle_email_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    status = data.get("change", False)
    lang = data.get("lang", "ru")

    email = message.text.strip()
    if not re.match(EMAIL_REGEX, email):
        await message.answer(text=getstr(lang, prefix, "error.wrong_email.caption"))
        return

    if not status and not isinstance(get_user_by_email(email), type(None)):
        await message.answer(text=getstr(lang, prefix, "error.wrong_email.email_already_used_caption"))
        return

    verification_code = str(random.randint(100000, 999999))
    VERIFICATION_CODES[message.from_user.id] = {
        "code": verification_code,
        "expires": datetime.now() + timedelta(minutes=15)
    }

    email_sent = await send_verification_email(email, verification_code, lang)

    if not email_sent:
        await message.answer(text=getstr(lang, prefix, "error.sending_code_error.caption"))
        return

    await state.update_data(email=email)
    await message.answer(text=getstr(lang, prefix, "email_confirm.caption"))
    await state.set_state(RegisterStates.waiting_for_verification_code)


async def pr_cb_handle_verification_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    email = data.get("email", SMTP_USERNAME)
    user_code = message.text.strip()
    user_id = message.from_user.id

    if user_id not in VERIFICATION_CODES or datetime.now() > VERIFICATION_CODES[user_id]["expires"]:
        await message.answer(text=getstr(lang, prefix, "email_confirm.code_expired_caption"))
        await state.clear()
        return

    if user_code == VERIFICATION_CODES[user_id]["code"]:
        data = await state.get_data()
        status = data.get("change", False)

        del VERIFICATION_CODES[user_id]

        if status:
            await pr_cb_change_user_info_db(message, state)
        else:
            await pr_cb_add_user_to_db(message, state)
    else:
        await message.answer(text=getstr(lang, prefix, "error.wrong_code.caption"))


async def send_verification_email(email: str, code: str, lang: str):
    """Sends an email with a confirmation code"""
    msg = MIMEText(
        f"{getstr(lang, prefix, "email_confirm.email_text_caption_part1")} {code}\n\n"
        f"{getstr(lang, prefix, "email_confirm.email_text_caption_part2")}"
    )
    msg['Subject'] = getstr(lang, prefix, "email_confirm.email_subject_caption")
    msg['From'] = EMAIL_FROM
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


async def pr_cb_add_user_to_db(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    tg_name = message.from_user.username or f"id{message.from_user.id}"
    success = register_user_from_state(data, tg_name)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.button(
        text=getstr(lang, prefix, "change_info"), callback_data="pr_cb_change_user_fio"
    )

    if success:
        await message.answer(
            f"{getstr(lang, prefix, 'success.reg_caption')}\n\n"
            f"{getstr(lang, prefix, 'show_info.fio')}: {data.get('fio')}\n"
            f"{getstr(lang, prefix, 'show_info.phone')}: {data.get('phone')}\n"
            f"{getstr(lang, prefix, 'show_info.email')}: {data.get('email')}",
            reply_markup=keyboard.as_markup(),
        )
    else:
        await message.answer(
            getstr(lang, prefix, "error.db_error.caption"),
            reply_markup=keyboard.as_markup(),
        )

    await state.clear()


# Change user ---------------------------------------------------------------------------------
async def pr_cb_change_user_fio(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await callback_query.message.edit_text(text=getstr(lang, prefix, "fio"))
    await state.set_state(RegisterStates.fio)


async def pr_cb_change_user_info_db(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    tg_name = message.from_user.username or f"id{message.from_user.id}"
    success = update_user_from_state(data, tg_name)

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.button(
        text=getstr(lang, prefix, "change_info"), callback_data="pr_cb_change_user_fio"
    )

    if success:
        await message.answer(
            f"{getstr(lang, prefix, 'success.change_caption')}\n\n"
            f"{getstr(lang, prefix, 'show_info.fio')}: {data.get('fio')}\n"
            f"{getstr(lang, prefix, 'show_info.phone')}: {data.get('phone')}\n"
            f"{getstr(lang, prefix, 'show_info.email')}: {data.get('email')}",
            reply_markup=keyboard.as_markup(),
        )
    else:
        await message.answer(
            getstr(lang, prefix, "error.db_error.caption"),
            reply_markup=keyboard.as_markup(),
        )

    await state.clear()
