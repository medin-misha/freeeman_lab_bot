from aiogram.fsm.state import State, StatesGroup


class MoreStates(StatesGroup):
    shop = State()
    services = State()
    consultations = State()
    regressions = State()
    mentorship = State()
