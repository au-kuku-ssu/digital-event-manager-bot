from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from components.participant_drawer.db.database import Database as pd_db
from components.participant_drawer.features.activities.data import (
    SAVE_BUTTON_NAME,
    YAML_PATH,
)
from components.participant_drawer.features.activities.fsm_states import (
    CommitteeAddingStates as AddingStates,
)
from components.participant_drawer.features.activities.fsm_states import (
    CommitteeEditingStates as EditingStates,
)
from components.participant_drawer.features.activities.keyboards import (
    CommitteeKeyboards as Keyboards,
)
from components.participant_drawer.features.activities.prefixes import (
    ActivitiesPrefixes,
)
from components.participant_drawer.features.activities.prefixes import (
    CommitteePrefixes as Prefixes,
)
from components.participant_drawer.tools import getstr
from components.shared.db import Database

router = Router()


@router.callback_query(lambda c: c.data == f"{Prefixes.PREFIX}menu")
async def cb_pd_committee_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext, activity: str
) -> None:
    """ """
    lang = "ru"
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.committee.add"),
        callback_data=f"{Prefixes.PREFIX}add",
    )
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.committee.edit"),
        callback_data=f"{Prefixes.PREFIX}edit",
    )
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.committee.get"),
        callback_data=f"{Prefixes.PREFIX}get",
    )
    keyboard.button(
        text=getstr(lang, f"{YAML_PATH}.committee.back"),
        callback_data=f"{ActivitiesPrefixes.PREFIX}choose",
    )
    keyboard.adjust(1)
    await callback_query.message.edit_text(
        getstr(lang, f"{YAML_PATH}.committee.caption"),
        reply_markup=keyboard.as_markup(),
    )


# ____________________________ ADD ____________________________


@router.callback_query(lambda c: c.data == f"{Prefixes.PREFIX}break")
async def cb_pd_add_committee_participant_break(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, activity: str
) -> None:
    await state.clear()
    await cb_pd_committee_menu(callback_query, bot, state, activity)


@router.callback_query(lambda c: c.data == f"{Prefixes.PREFIX}add")
async def cb_pd_add_committee_participant(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, activity: str
) -> None:
    await state.set_state(AddingStates.name)
    await state.update_data(message_id=callback_query.message.message_id)
    button = Keyboards.get_process_break_button(
        getstr("ru", f"{YAML_PATH}.committee.break")
    )
    await callback_query.message.edit_text(
        text=getstr("ru", f"{YAML_PATH}.committee.full_name"), reply_markup=button
    )


@router.message(AddingStates.name)
async def cb_pd_add_committee_participant_name(
    message: types.Message, bot: Bot, state: FSMContext, activity: str
) -> None:
    full_name = message.text.split()
    if len(full_name) < 2:
        message_id = await state.get_value("message_id")
        button = Keyboards.get_process_break_button(
            getstr("ru", f"{YAML_PATH}.committee.break")
        )
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=getstr("ru", f"{YAML_PATH}.committee.name"),
            reply_markup=button,
        )
        await message.delete()
        return

    await state.update_data(
        first_name=full_name[0],
        last_name=full_name[1],
        middle_name="".join(full_name[2:]) if len(full_name) == 3 else "",
    )
    await state.set_state(AddingStates.degree)

    message_id = await state.get_value("message_id")
    button = Keyboards.get_process_break_button(
        getstr("ru", f"{YAML_PATH}.committee.break")
    )
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=getstr("ru", f"{YAML_PATH}.committee.degree"),
        reply_markup=button,
    )
    await message.delete()


@router.message(AddingStates.degree)
async def cb_pd_add_committee_participant_degree(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(degree=message.text)
    await state.set_state(AddingStates.title)

    message_id = await state.get_value("message_id")
    button = Keyboards.get_process_break_button(
        getstr("ru", f"{YAML_PATH}.committee.break")
    )
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=getstr("ru", f"{YAML_PATH}.committee.title"),
        reply_markup=button,
    )
    await message.delete()


@router.message(AddingStates.title)
async def cb_pd_add_committee_participant_title(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddingStates.position)

    message_id = await state.get_value("message_id")
    button = Keyboards.get_process_break_button(
        getstr("ru", f"{YAML_PATH}.committee.break")
    )
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=getstr("ru", f"{YAML_PATH}.committee.position"),
        reply_markup=button,
    )
    await message.delete()


@router.message(AddingStates.position)
async def cb_pd_add_committee_participant_position(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(position=message.text)
    await state.set_state(AddingStates.contact_info)

    message_id = await state.get_value("message_id")
    button = Keyboards.get_process_break_button(
        getstr("ru", f"{YAML_PATH}.committee.break")
    )
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=getstr("ru", f"{YAML_PATH}.committee.contact_info"),
        reply_markup=button,
    )
    await message.delete()


@router.message(AddingStates.contact_info)
async def cb_pd_add_committee_participant_contact_info(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr("ru", f"{YAML_PATH}.committee.reject"),
        callback_data=f"{Prefixes.PREFIX}break",
    )
    keyboard.button(
        text=getstr("ru", f"{YAML_PATH}.committee.accept"),
        callback_data=f"{Prefixes.ADD}accept",
    )
    keyboard.adjust(1)

    await state.update_data(contact_number=message.text)
    data = await state.get_data()
    name = f"{data['first_name']} {data['last_name']} {data['middle_name']}"
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["message_id"],
        text=
        f"""
        {getstr("ru", f"{YAML_PATH}.committee.full_name")}: {name}
        {getstr("ru", f"{YAML_PATH}.committee.degree")}: {data["degree"]}
        {getstr("ru", f"{YAML_PATH}.committee.title")}: {data["title"]}
        {getstr("ru", f"{YAML_PATH}.committee.position")}: {data["position"]}
        {getstr("ru", f"{YAML_PATH}.committee.contact_info")}: {data["contact_number"]}
        """,
        reply_markup=keyboard.as_markup(),
    )
    await message.delete()


@router.callback_query(lambda c: c.data == f"{Prefixes.ADD}accept")
async def cb_pd_add_committee_participant_accept(
    callback_query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    db: Database,
    activity: str,
) -> None:
    # Добавление в бд
    # ...
    # module_kobanius.insert_to_committee(participant)

    data = await state.get_data()
    data.pop("message_id")
    contact_number = data.pop("contact_number")

    # id = pd_db.insert(db, "people", data)
    # pd_db.insert(db, "organizers", {"id": id, "contact_number": contact_number})
    await state.clear()
    await cb_pd_committee_menu(callback_query, bot, state, activity)


# ____________________________ EDIT ____________________________


@router.callback_query(lambda c: c.data == f"{Prefixes.PREFIX}edit")
async def cb_pd_edit_committee_participant(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db
) -> None:
    participants: dict[str, int] = None
    # Взять из базы список с именами и их id
    # он должен лежать в participants
    # ...
    # state
    # participants = pd_db.select(
    #     db, "peoples", ["id", "first_name", "last_name", "middle_name"]
    # )
    buttons = Keyboards.get_committee_participants_keyboard(participants)
    await callback_query.message.answer(
        text="Выберите участника",
        reply_markup=buttons,
    )


@router.callback_query(F.data.startswith(Prefixes.EDIT_CHOOSE_PARTICIPANT))
async def cb_pd_edit_committee_choose_participant(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    id = int(callback_query.data.split("_")[-1])
    fields = [
        getstr("ru", f"{YAML_PATH}.committee.full_name"),
        getstr("ru", f"{YAML_PATH}.committee.title"),
        getstr("ru", f"{YAML_PATH}.committee.degree"),
    ]
    buttons = Keyboards.get_committee_participant_data(
        id,
        fields,
        SAVE_BUTTON_NAME,
    )
    await callback_query.message.answer(
        text="Выберите, что вам нужно изменить", reply_markup=buttons
    )


@router.callback_query(F.data.startswith(Prefixes.EDIT_CHOOSE_PARTICIPANT))
async def cb_pd_edit_committee_participant_choose_field(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    id = int(callback_query.data.split("_")[-1])
    field = callback_query.data.split("_")[-2]

    await callback_query.message.answer(text=f"Enter new {field}:", reply_markup=None)
    await state.update_data(participant_id=id)
    await state.set_state(EditingStates.name)


@router.message(EditingStates.name)
async def cb_pd_edit_committee_participant_name(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(name=message.text)


@router.message(EditingStates.degree)
async def cb_pd_edit_committee_participant_degree(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(degree=message.text)


@router.message(EditingStates.title)
async def cb_pd_edit_committee_participant_rank(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(rank=message.text)


@router.message(EditingStates.position)
async def cb_pd_edit_committee_participant_position(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(position=message.text)


@router.message(EditingStates.contact_info)
async def cb_pd_edit_committee_participant_contact_info(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(contact_info=message.text)


@router.callback_query(
    lambda cbk: cbk.data == f"{Prefixes.EDIT_CHOOSE_FIELD}{SAVE_BUTTON_NAME}"
)
async def cb_pd_edit_committee_participant_save(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext, db
) -> None:
    participant_changes = await state.get_data()
    # Сохранение изменений в БД
    # ...
    pd_db.update(db, participant_changes)

    await state.clear()
    await callback_query.message.answer(text="Saved")

    # await callback_query.message.answer(
    #     text=f"""
    #     ФИО: {participant_changes["name"]}
    #     Степень: {participant_changes["degree"]}
    #     Звание: {participant_changes["rank"]}
    #     Должность: {participant_changes["position"]}
    #     Контактная информация: {participant_changes["contact_info"]}
    #     """
    # )


# ____________________________ GET ____________________________


@router.callback_query(lambda c: c.data == f"{Prefixes.PREFIX}get")
async def cb_pd_get_committee_participant(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    participant: dict = None
    # Получить данные из БД
    # ...

    await callback_query.message.answer(
        text=f"""
        ФИО: {participant["name"]}
        Степень: {participant["degree"]}
        Звание: {participant["rank"]}
        Должность: {participant["position"]}
        Контактная информация: {participant["contact_info"]}
        """
    )


async def frontend_cb_pd_get_committee_participants(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    participants: list[str] = None
    # Получить имена из БД
    # ...
    await callback_query.message.answer("\n".join(participants))


# ____________________________ DELETE ____________________________
