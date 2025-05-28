from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from components.organizer_mode.features.activities.data import (
    ACTIVITY_DATA_NAME,
    YAML_PATH,
)
from components.organizer_mode.features.activities.prefixes import (
    ActivitiesPrefixes as Prefixes,
    ACTIVITIES_PREFIX, 
)
from components.organizer_mode.features.activities.prefixes import CommitteePrefixes
from components.organizer_mode.tools import getstr
from components.organizer_mode.prefixes import PREFIX

router = Router()


@router.callback_query(lambda c: c.data == f"{ACTIVITIES_PREFIX}main")
async def cb_om_activity_choosing(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """ """
    lang = "ru"
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="activity1",
        callback_data=f"{Prefixes.PREFIX}choose_activity1",
    )
    keyboard.button(
        text="activity2",
        callback_data=f"{Prefixes.PREFIX}choose_activity2",
    )
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.back"), 
        callback_data=f"{PREFIX}main",
    )

    keyboard.adjust(1)
    await callback_query.message.edit_text(
        getstr(lang, f"{YAML_PATH}.caption"), reply_markup=keyboard.as_markup()
    )    


@router.callback_query(F.data.startswith(f"{Prefixes.PREFIX}choose"))
async def cb_om_activity_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    lang = "ru"
    activity_name = callback_query.data.split("_")[-1]
    await state.update_data(**{ACTIVITY_DATA_NAME: activity_name})
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.committee.caption"),
        callback_data=f"{CommitteePrefixes.PREFIX}menu",
    )
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.back"), 
        callback_data=f"{ACTIVITIES_PREFIX}main"
    )
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, f"{YAML_PATH}.caption"), reply_markup=keyboard.as_markup()
    )
