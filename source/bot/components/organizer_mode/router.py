from aiogram import Bot, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from components.organizer_mode.features.activities import activity_router
from components.organizer_mode.features.applicationsService import applications_router
from components.organizer_mode.prefixes import ACTIVITIES_PREFIX, PREFIX, APPLICATION_PREFIX
from components.organizer_mode.tools import getstr


def unite_routers() -> Router:
    router = Router()
    router.include_routers(activity_router, applications_router)
    return router


router = unite_routers()


@router.callback_query(lambda c: c.data == f"{PREFIX}main")
async def cb_om_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
    lang = "ru"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, "organizer_mode.main.back"), callback_data="cb_mm_main"
    )
    keyboard.button(
        text=getstr(lang, "organizer_mode.activities.caption"),
        callback_data=f"{ACTIVITIES_PREFIX}main",
    )
    keyboard.button(
      text=getstr(lang, "organizer_mode.applications.caption"),
      callback_data=f"{APPLICATION_PREFIX}"
    )

    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, "organizer_mode.main.caption"),
        reply_markup=keyboard.as_markup(),
    )
