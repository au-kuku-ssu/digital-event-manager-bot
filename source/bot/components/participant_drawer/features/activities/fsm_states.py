from aiogram.fsm.state import State, StatesGroup


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
