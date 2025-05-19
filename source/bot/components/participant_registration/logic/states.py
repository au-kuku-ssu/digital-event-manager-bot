from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    fio = State()
    phone = State()
    email = State()
    waiting_for_verification_code = State()
