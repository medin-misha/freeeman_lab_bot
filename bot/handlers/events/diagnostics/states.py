from aiogram.fsm.state import State, StatesGroup


class DiagnosticStates(StatesGroup):
    waiting_for_audio = State()
    waiting_for_diagnostic_type = State()
    waiting_for_description = State()
    confirmation = State()
    waiting_for_file_confirmation = State()
