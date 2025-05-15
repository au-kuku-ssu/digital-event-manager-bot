from aiogram.fsm.state import State, StatesGroup


# Состояния для FSM
class EventsStates(StatesGroup):
    waiting_for_edit_choice = State()
    waiting_for_edit_value = State()
    waiting_for_delete_confirmation = State()


class CommitteeAddingStates(StatesGroup):
    name = State()
    degree = State()
    rank = State()
    position = State()
    contact_info = State()


class CommitteeEditingStates(StatesGroup):
    name = State()
    degree = State()
    rank = State()
    position = State()
    contact_info = State()
