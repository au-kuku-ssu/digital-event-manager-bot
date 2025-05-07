from aiogram.fsm.state import State, StatesGroup


class REAuthStates(StatesGroup):
    waiting_for_code = State()
    authorized = State()


class REEvaluationStates(StatesGroup):
    waiting_for_comment = State()
    comment_added = State()
    marks_accepted = State()
