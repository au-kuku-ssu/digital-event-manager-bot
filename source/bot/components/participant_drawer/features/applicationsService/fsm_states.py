from aiogram.fsm.state import State, StatesGroup


# Состояния для FSM
class ApplicationStates(StatesGroup):
    waiting_for_edit_choice = State()
    waiting_for_edit_value = State()
    waiting_for_edit_finish = State()
    waiting_for_delete_confirmation = State()
