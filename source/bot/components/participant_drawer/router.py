from aiogram import Bot, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from components.participant_drawer.features.activities import activity_router
from components.participant_drawer.prefixes import PREFIX
from components.participant_drawer.tools import getstr


def unite_routers() -> Router:
    router = Router()
    router.include_routers((activity_router))
    return router


router = unite_routers()


@router.callback_query(lambda c: c.data == f"{PREFIX}main")
async def cb_pd_main_menu(callback_query: types.CallbackQuery, bot: Bot) -> None:
    lang = "ru"

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, "participant_drawer.main.back"), callback_data="cb_mm_main"
    )
    keyboard.button(
        text=getstr(lang, "participant_drawer.committee"),
        callback_data="cb_pd_committee",
    )

    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, "participant_drawer.main.caption"),
        reply_markup=keyboard.as_markup(),
    )
