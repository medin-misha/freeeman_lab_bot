from aiogram.fsm.state import State, StatesGroup


class AnalysisStates(StatesGroup):
    choosing_format = State()
    public_intro = State()
    private_intro = State()
    public_schedule = State()
    private_schedule = State()
