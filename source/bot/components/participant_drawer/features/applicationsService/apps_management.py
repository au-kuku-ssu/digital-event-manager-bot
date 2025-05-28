from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from components.participant_drawer.features.applicationsService.fsm_states import ApplicationStates
from components.participant_drawer.features.applicationsService.prefixes import ApplicationPrefixes
from components.participant_drawer.features.applicationsService.keyboards import (kb_change_status, kb_change_app,
                                                                                      kb_delete_app, kb_application_menu,
                                                                                      kb_back_to_menu)


router = Router()


@router.callback_query(lambda c: c.data == ApplicationPrefixes.PREFIX)
@router.message(F.text == "Меню обработки заявок")
async def cb_pd_application_menu(callback: CallbackQuery | Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Управление заявками участников:", reply_markup=kb_application_menu())


# ____________________________ Approving ____________________________


# Список заявок с возможностью подтверждения
@router.callback_query(lambda c: c.data == f"{ApplicationPrefixes.LIST}")
async def cb_pd_application_list(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    # Здесь должна быть логика получения заявок из БД
    # applications = await db.get_data(["id", "name", "event", "topic", "faculty",
    #                                   "degree", "translator", "contact", "status"])

    # Заглушка с тестовыми данными
    applications = [
        {"id": 1, "name": "Иван Иванов", "event": "Конференция AI", "topic": "Фурье-преобразование", "faculty": "фКНиИТ",
         "degree": "магистр 1 курса", "translator": "Есть", "contact": "ivan@example.com", "status": "pending"},
        {"id": 2, "name": "Петр Петров", "event": "Воркшоп Python", "topic": "Терагерцовое излучение", "faculty": "Инфиз",
         "degree": "магистр 2 курса", "translator": "Есть", "contact": "+79123456789", "status": "approved"},
        {"id": 3, "name": "Сергей Иванов", "event": "Конференция AI", "topic": "Фурье-преобразование", "faculty": "фКНиИТ",
         "degree": "магистр 1 курса", "translator": "Есть", "contact": "ivan@example.com", "status": "pending"},
        {"id": 4, "name": "Алексей Петров", "event": "Воркшоп Python", "topic": "Терагерцовое излучение", "faculty": "Инфиз",
         "degree": "магистр 2 курса", "translator": "Есть", "contact": "+79123456789", "status": "approved"}
    ]

    if not applications:
        await callback.answer("Нет активных заявок")

    await callback.message.answer("Список заявок:")

    for app in applications:
        status_emoji = "🕒"
        kb = InlineKeyboardMarkup(inline_keyboard=[])

        if app['status'] == 'approved':
            status_emoji = "✅"
            kb = InlineKeyboardMarkup(inline_keyboard=[])
        elif app['status'] == 'pending':
            status_emoji = "🕒"
            kb = kb_change_status(app['id'])

        await callback.message.answer(
            f"""
            {status_emoji} Заявка #{app['id']}\n
            Участник: {app['name']}\n
            Мероприятие: {app['event']}\n
            Тема доклада: {app['topic']}\n
            Образование: {app['degree']}\n
            Наличие образования переводчика: {app['translator']}\n
            Контактная информация: {app['contact']}\n
            Статус: {'Подтверждено' if app['status'] == 'approved' else 'Ожидает подтверждения'}
            """, reply_markup=kb
        )

    await callback.message.answer("Управление заявками участников:", reply_markup=kb_application_menu())


# Подтверждение заявки
@router.callback_query(lambda c: c.data.startswith(f"{ApplicationPrefixes.APPROVE}"))
async def cb_pd_application_approve(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    app_id = int(callback.data.split(f"{ApplicationPrefixes.APPROVE}")[1])
    # Здесь должна быть логика обновления статуса в БД
    # await db.change_status(app_id, 'approved')

    await callback.message.edit_text(
        callback.message.text.replace("🕒", "✅").replace("Ожидает подтверждения", "Подтверждена")
    )
    await callback.answer("Заявка подтверждена")


# Отклонение заявки
@router.callback_query(lambda c: c.data.startswith(f"{ApplicationPrefixes.REJECT}"))
async def cb_pd_application_reject(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    app_id = int(callback.data.split(f"{ApplicationPrefixes.REJECT}")[1])
    # Здесь должна быть логика обновления статуса в БД
    # await db.change_status(app_id, 'rejected')

    await callback.message.edit_text(
        callback.message.text.replace("🕒", "❌").replace("Ожидает подтверждения", "Отклонена")
    )
    await callback.answer("Заявка отклонена")


# ____________________________ Delete ____________________________


# Удаление заявки - шаг 1: выбор ID
@router.callback_query(lambda c: c.data == f"{ApplicationPrefixes.DELETE}")
async def cb_pd_application_delete_start(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.message.edit_text("Введите ID заявки для удаления:", reply_markup=kb_back_to_menu())
    await state.set_state(ApplicationStates.waiting_for_delete_confirmation)
    await callback.answer()


# Удаление заявки - подтверждение и выполнение
@router.message(ApplicationStates.waiting_for_delete_confirmation)
async def cb_pd_application_delete_confirm(message: Message, bot: Bot, state: FSMContext) -> None:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    try:
        app_id = int(message.text)

        # Здесь должна выполняться проверка существования заявки в БД
        id_list = await db.get_data(['id'])
        id_exists = any(value.get("name") == app_id for value in id_list)
        if id_exists:
            kb = kb_delete_app(app_id)

        await message.answer(
            f"Вы уверены, что хотите удалить заявку #{app_id}?",
            reply_markup=kb
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID заявки.")


# Подтверждение удаления
@router.callback_query(F.data.startswith(f"{ApplicationPrefixes.DELETE}"))
@router.callback_query(F.data.endswith("confirm"))
async def cb_pd_application_delete_final(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    app_id = int(callback.data.split("_")[-2])
    # Здесь должна быть логика удаления из БД
    # await db.delete_app(app_id)

    await callback.answer(f"Заявка #{app_id} удалена.")


# Отмена удаления
@router.callback_query(lambda c: c.data == f"{ApplicationPrefixes.DELETE}cancel")
async def cb_pd_application_delete_cancel(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.answer("Удаление отменено.")


# ____________________________ Editing ____________________________


# Редактирование заявки - шаг 1: выбор ID
@router.callback_query(lambda c: c.data == f"{ApplicationPrefixes.EDIT}")
async def cb_pd_application_edit_start(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.message.edit_text("Введите ID заявки для редактирования:", reply_markup=kb_back_to_menu())
    await state.set_state(ApplicationStates.waiting_for_edit_choice)


# Редактирование заявки - шаг 2: выбор поля
@router.message(ApplicationStates.waiting_for_edit_choice)
async def cb_pd_application_edit_choose_field(message: Message, bot: Bot, state: FSMContext) -> None:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    try:
        app_id = int(message.text)
        # Здесь должна быть проверка существования заявки в БД
        # id_list = await db.get_data(['id'])

        # Заглушка с тестовыми данными
        id_list = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}]

        id_exists = any(value.get("id") == app_id for value in id_list)
        if id_exists:
            kb = kb_change_app()

        await state.update_data(app_id=app_id)

        await message.answer(
            f"Что вы хотите изменить в заявке #{app_id}?",
            reply_markup=kb
        )
        await state.set_state(ApplicationStates.waiting_for_edit_value)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID заявки.")


# Редактирование заявки - шаг 3: ввод нового значения
@router.callback_query(ApplicationStates.waiting_for_edit_value)
@router.callback_query(F.data.startswith(f"{ApplicationPrefixes.EDIT}"))
async def cb_pd_application_edit_get_value(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    field = callback.data.split(f"{ApplicationPrefixes.EDIT}")[1]
    await state.update_data(field=field)
    await state.set_state(ApplicationStates.waiting_for_edit_finish)
    await callback.message.edit_text(f"Введите новое значение для поля {field}:")


# Редактирование заявки - финал (здесь должна быть логика обновления в БД)
@router.message(ApplicationStates.waiting_for_edit_finish)
async def cb_pd_application_edit_finish(message: Message, bot: Bot, state: FSMContext) -> None:

    user_data = await state.get_data()
    app_id = user_data['app_id']
    field = user_data['field']
    new_value = message.text

    # Здесь должна быть логика обновления в БД
    # await db.update_app_field(app_id, field, new_value)

    # Заглушка с тестовыми данными
    applications = [
      {"id": 1, "name": "Иван Иванов", "event": "Конференция AI", "section": "Тестовая секция №1",
       "presentation_topic": "Фурье-преобразование", "faculty": "фКНиИТ", "degree": "магистр 1 курса",
       "teacher": "Сергеев Сергей Сергеевич", "has_translator_education": "Есть", "is_translator_participate": "Нет",
       "english_book": "Choices Upper Intermediate", "email": "ivan@example.com"},
      {"id": 2, "name": "Петр Петров", "event": "Воркшоп Python", "section": "Тестовая секция №1",
       "presentation_topic": "Терагерцовое излучение", "faculty": "Инфиз", "degree": "магистр 2 курса",
       "teacher": "Сергеев Сергей Сергеевич", "has_translator_education": "Есть", "is_translator_participate": "Нет",
       "english_book": "Choices Upper Intermediate","email": "petr@example.com"},
      {"id": 3, "name": "Сергей Иванов", "event": "Конференция AI", "section": "Тестовая секция №1",
       "presentation_topic": "Фурье-преобразование", "faculty": "фКНиИТ", "degree": "магистр 1 курса",
       "teacher": "Сергеев Сергей Сергеевич", "has_translator_education": "Есть", "is_translator_participate": "Нет",
       "english_book": "Choices Upper Intermediate","email": "sergei@example.com"},
      {"id": 4, "name": "Алексей Петров", "event": "Воркшоп Python", "section": "Тестовая секция №1",
       "presentation_topic": "Терагерцовое излучение", "faculty": "Инфиз", "degree": "магистр 2 курса",
       "teacher": "Сергеев Сергей Сергеевич", "has_translator_education": "Есть", "is_translator_participate": "Нет",
       "english_book": "Choices Upper Intermediate","email": "alexei@example.com"}
    ]

    for app in applications:
        if app.get("id") == app_id:
            app[f"{field}"] = new_value
            break

    await message.answer(f"""
        Заявка #{app_id} обновлена:\n
        Поле {field} изменено на: {new_value}
        """, reply_markup=kb_back_to_menu()
    )
    await state.clear()
