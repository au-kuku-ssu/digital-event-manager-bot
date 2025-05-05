from aiogram.fsm.state import State, StatesGroup


class REAuthStates(StatesGroup):
    waiting_for_code = State()
    authorized = State()
