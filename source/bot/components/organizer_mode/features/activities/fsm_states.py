from aiogram.fsm.state import State, StatesGroup


class CommitteeAddingStates(StatesGroup):
    name = State()
    degree = State()
    title = State()
    position = State()
    contact_info = State()


class CommitteeEditingStates(StatesGroup):
    name = State()
    degree = State()
    title = State()
    position = State()
    contact_info = State()
