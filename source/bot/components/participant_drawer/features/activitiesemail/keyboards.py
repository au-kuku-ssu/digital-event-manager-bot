from aiogram.utils.keyboard import ReplyKeyboardBuilder
from components.participant_drawer.features.activities.prefixes import CommitteePrefixes


class CommitteeKayboards:
    def get_committee_member_data(id: int, fields: list[str], save_button_name: str):
        keyboard = ReplyKeyboardBuilder()
        for name in fields:
            cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_FIELD}{name}_{id}"
            keyboard.button(text=name, callback_data=cbk_data)

        cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_FIELD}{save_button_name}_{id}"
        keyboard.button(text=f"{save_button_name}", callback_data=cbk_data)

        keyboard.adjust(1)
        return keyboard

    def get_committee_members_keyboard(members: dict[int, str]):
        keyboard = ReplyKeyboardBuilder()
        for id, name in members.items():
            cbk_data = f"{CommitteePrefixes.EDIT_CHOOSE_MEMBER}{name}_{id}"
            keyboard.button(text=name, callback_data=cbk_data)

        keyboard.adjust(1)
        return keyboard
