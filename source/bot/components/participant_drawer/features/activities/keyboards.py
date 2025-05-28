from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup
from components.participant_drawer.features.activities.prefixes import CommitteePrefixes


class CommitteeKeyboards:
    def get_process_break_button(button_text: str) -> ReplyKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(
            text=button_text, callback_data=f"{CommitteePrefixes.PREFIX}break"
        )
        return keyboard.as_markup()

    def get_committee_participant_data(
        id: int, fields: list[str], save_button_name: str
    ):
        keyboard = InlineKeyboardBuilder()
        for name in fields:
            cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_FIELD}{name}_{id}"
            keyboard.button(text=name, callback_data=cbk_data)

        cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_FIELD}{save_button_name}_{id}"
        keyboard.button(text=save_button_name, callback_data=cbk_data)

        keyboard.adjust(1)
        return keyboard

    def get_committee_participants_keyboard(participants: dict[int, str]):
        keyboard = InlineKeyboardBuilder()
        for id, name in participants.items():
            cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_PARTICIPANT}{name}_{id}"
            keyboard.button(text=name, callback_data=cbk_data)

        keyboard.adjust(1)
        return keyboard
