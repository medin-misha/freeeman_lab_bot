from aiogram.fsm.state import State, StatesGroup

class DiagnosticStates(StatesGroup):
    waiting_for_audio = State()
    confirmation = State()