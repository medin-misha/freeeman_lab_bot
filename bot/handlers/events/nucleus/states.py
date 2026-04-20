from aiogram.fsm.state import State, StatesGroup


class NucleusStates(StatesGroup):
    intro = State()
    inside = State()
    how_to_join = State()
    waiting_for_application = State()
