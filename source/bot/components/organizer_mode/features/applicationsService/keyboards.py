from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from components.organizer_mode.prefixes import PREFIX
from source.bot.components.organizer_mode.features.applicationsService.prefixes import ApplicationPrefixes


# Меню управления заявками
def kb_application_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="Список заявок", callback_data=f"{ApplicationPrefixes.LIST}")],
      [InlineKeyboardButton(text="Изменить заявку", callback_data=f"{ApplicationPrefixes.EDIT}")],
      [InlineKeyboardButton(text="Удалить заявку", callback_data=f"{ApplicationPrefixes.DELETE}")],
      [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{PREFIX}main")]
    ])

    return keyboard


# Возврат в меню обработки заявок
def kb_back_to_menu():
  return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В управления заявками",
                                                                     callback_data=f"{ApplicationPrefixes.PREFIX}")]])


# Клавиатура для изменения статуса заявки
def kb_change_status(app_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data=f"{ApplicationPrefixes.APPROVE}{app_id}")],
            [InlineKeyboardButton(text="Отклонить", callback_data=f"{ApplicationPrefixes.REJECT}{app_id}")]
    ])

    return keyboard


# Клавиатура для подтверждения удаления заявки
def kb_delete_app(app_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data=f"{ApplicationPrefixes.DELETE}{app_id}_confirm")],
        [InlineKeyboardButton(text="Нет", callback_data=f"{ApplicationPrefixes.DELETE}cancel")],
        [InlineKeyboardButton(text="В меню управления заявками", callback_data=f"{ApplicationPrefixes.PREFIX}")]
    ])
    return keyboard


# Клавиатура для полей требующих изменения
def kb_change_app():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data=f"{ApplicationPrefixes.EDIT}name")],
        [InlineKeyboardButton(text="Мероприятие", callback_data=f"{ApplicationPrefixes.EDIT}event")],
        [InlineKeyboardButton(text="Факультет", callback_data=f"{ApplicationPrefixes.EDIT}faculty")],
        [InlineKeyboardButton(text="Образование", callback_data=f"{ApplicationPrefixes.EDIT}degree")],
        [InlineKeyboardButton(text="Учитель", callback_data=f"{ApplicationPrefixes.EDIT}teacher")],
        [InlineKeyboardButton(text="Секция", callback_data=f"{ApplicationPrefixes.EDIT}section")],
        [InlineKeyboardButton(text="Тема", callback_data=f"{ApplicationPrefixes.EDIT}presentation_topic")],
        [InlineKeyboardButton(text="Учебник английского", callback_data=f"{ApplicationPrefixes.EDIT}english_book")],
        [InlineKeyboardButton(text="Участие в переводчиках", callback_data=f"{ApplicationPrefixes.EDIT}is_translator_participate")],
        [InlineKeyboardButton(text="Наличие диплома переводчика", callback_data=f"{ApplicationPrefixes.EDIT}has_translator_education")],
        [InlineKeyboardButton(text="Почта", callback_data=f"{ApplicationPrefixes.EDIT}email")],
        [InlineKeyboardButton(text="В меню управления заявками", callback_data=f"{ApplicationPrefixes.PREFIX}")]
    ])

    return keyboard
