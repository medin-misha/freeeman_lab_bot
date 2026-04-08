from aiogram.fsm.state import State, StatesGroup


class FSMError(StatesGroup):
    error = State()
