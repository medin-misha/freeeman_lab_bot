from aiogram.fsm.state import State, StatesGroup


class DiagnosticStates(StatesGroup):
    waiting_for_result_file = State()
