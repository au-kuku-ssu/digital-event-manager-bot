from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    fio = State()
    phone = State()
    email = State()
