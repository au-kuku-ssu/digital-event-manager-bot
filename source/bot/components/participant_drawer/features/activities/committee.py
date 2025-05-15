from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from components.participant_drawer.features.committee.keyboards import (
    get_committee_member_data,
    get_committee_members_keyboard,
)
from components.participant_drawer.features.activities.prefixes import CommitteePrefixes
from components.participant_drawer.features.activities.fsm_states import (
    CommitteeAddingStates,
    CommitteeEditingStates,
)

router = Router()
SAVE_BUTTON_NAME = "save"


@router.callback_query(lambda c: c.data == CommitteePrefixes.PREFIX)
async def cb_pd_committee_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """ """
    pass


# ____________________________ ADD ____________________________


@router.callback_query(lambda c: c.data == f"{CommitteePrefixes.PREFIX}add")
async def cb_pd_add_committee_member(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.set_state(CommitteeAddingStates.name)
    await callback_query.message.answer(text="ФИО:")


@router.message(CommitteeAddingStates.name)
async def cb_pd_add_committee_member_name(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(name=message.text)
    await state.set_state(CommitteeAddingStates.degree)
    await message.answer(text="Степень:")


@router.message(CommitteeAddingStates.degree)
async def cb_pd_add_committee_member_degree(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(degree=message.text)
    await state.set_state(CommitteeAddingStates.rank)
    await message.answer(text="Степень:")


@router.message(CommitteeAddingStates.rank)
async def cb_pd_add_committee_member_rank(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(rank=message.text)
    await state.set_state(CommitteeAddingStates.position)
    await message.answer(text="Должность:")


@router.message(CommitteeAddingStates.position)
async def cb_pd_add_committee_member_position(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(position=message.text)
    await state.set_state(CommitteeAddingStates.contact_info)
    await message.answer(text="Контактная информация:")


@router.message(CommitteeAddingStates.contact_info)
async def cb_pd_add_committee_member_contact_info(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    member_data = await state.get_data()
    member_data.update(contact_info=message.text)
    # Добавление в бд
    # ...
    # module_kobanius.insert_to_committee(member_data)
    await state.clear()
    await message.answer("Добавление завершено")
    await message.answer(
        text=f"""
        ФИО: {member_data["name"]}
        Степень: {member_data["degree"]}
        Звание: {member_data["rank"]}
        Должность: {member_data["position"]}
        Контактная информация: {member_data["contact_info"]}
        """
    )


# ____________________________ EDIT ____________________________


@router.callback_query(lambda c: c.data == f"{CommitteePrefixes.PREFIX}edit")
async def cb_pd_edit_committee_member(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    members: dict[str, int] = None
    # Взять из базы список с именами и их id
    # он должен лежать в members
    # ...

    buttons = get_committee_members_keyboard(members)
    await callback_query.message.answer(
        text="Выберите участника",
        reply_markup=buttons,
    )


@router.callback_query(F.data.startswith(CommitteePrefixes.EDIT_CHOOSE_MEMBER))
async def cb_pd_edit_committee_choose_member(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    id = int(callback_query.data.split("_")[-1])
    fields = ["ФИО", "Должность", "Звание"]
    save_button_name = "save"
    buttons = get_committee_member_data(
        id,
        fields,
        save_button_name,
    )
    await callback_query.message.answer(
        text="Выберите, что вам нужно изменить", reply_markup=buttons
    )


@router.callback_query(F.data.startswith(CommitteePrefixes.EDIT_CHOOSE_MEMBER))
async def cb_pd_edit_committee_member_choose_field(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    id = int(callback_query.data.split("_")[-1])
    field = callback_query.data.split("_")[-2]
    await callback_query.message.answer(text=f"Enter new {field}:", reply_markup=None)
    await state.set_data(memder_id=id)
    await state.set_state(CommitteeEditingStates.name)


@router.message(CommitteeEditingStates.name)
async def cb_pd_edit_committee_member_name(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.set_data(name=message.text)


@router.message(CommitteeEditingStates.degree)
async def cb_pd_edit_committee_member_degree(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.set_data(degree=message.text)


@router.message(CommitteeEditingStates.rank)
async def cb_pd_edit_committee_member_rank(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.set_data(rank=message.text)


@router.message(CommitteeEditingStates.position)
async def cb_pd_edit_committee_member_position(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.set_data(position=message.text)


@router.message(CommitteeEditingStates.contact_info)
async def cb_pd_edit_committee_member_contact_info(
    message: types.Message, bot: Bot, state: FSMContext
) -> None:
    await state.set_data(contact_info=message.text)


@router.callback_query(
    lambda cbk: cbk.data
    == f"{CommitteePrefixes.EDIT_CHOOSE_FIELD_PREFIX}{SAVE_BUTTON_NAME}"
)
async def cb_pd_edit_committee_member_save(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    member_changes = await state.get_data()
    # Сохранение изменений в БД
    # ...
    await state.clear()
    await callback_query.message.answer(text="Saved")

    # await callback_query.message.answer(
    #     text=f"""
    #     ФИО: {member_changes["name"]}
    #     Степень: {member_changes["degree"]}
    #     Звание: {member_changes["rank"]}
    #     Должность: {member_changes["position"]}
    #     Контактная информация: {member_changes["contact_info"]}
    #     """
    # )


# ____________________________ GET ____________________________


@router.callback_query(lambda c: c.data == f"{CommitteePrefixes.PREFIX}get")
async def cb_pd_get_committee_member(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    member: dict = None
    # Получить данные из БД
    # ...
    await callback_query.message.answer(
        text=f"""
        ФИО: {member["name"]}
        Степень: {member["degree"]}
        Звание: {member["rank"]}
        Должность: {member["position"]}
        Контактная информация: {member["contact_info"]}
        """
    )


async def frontend_cb_pd_get_committee_members(
    callback_query: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    members: list[str] = None
    # Получить имена из БД
    # ...
    await callback_query.message.answer("\n".join(members))


# ____________________________ DELETE ____________________________
