from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from os.path import join, dirname
from source.bot.components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "..", "locale"))


def getstr(lang, prefix, path):
    return get_locale_str(locale, f"{lang}.{prefix}.{path}")


async def pr_cb_pre_main(callback_query: types.CallbackQuery, bot: Bot) -> None:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Участник", callback_data="pr_cb_main")
    keyboard.button(text="Администратор", callback_data="pr_cb_admin_main")

    await callback_query.message.edit_text(
        "[DEBUG] Выберите роль", reply_markup=keyboard.as_markup()
    )


async def pr_cb_main(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    prefix = "participant_registration.user.main"
    shared = "participant_registration.shared"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, prefix, "browse"), callback_data="pr_cb_user_browse"
    )
    keyboard.button(
        text=getstr(lang, prefix, "search"), callback_data="pr_cb_user_search"
    )
    keyboard.button(
        text=getstr(lang, prefix, "my_activities"),
        callback_data="pr_cb_user_my_activities",
    )
    keyboard.button(
        text=getstr(lang, prefix, "my_data"), callback_data="pr_cb_user_my_data"
    )
    keyboard.button(text=getstr(lang, shared, "back"), callback_data="cb_mm_main")

    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix, "caption"), reply_markup=keyboard.as_markup()
    )
