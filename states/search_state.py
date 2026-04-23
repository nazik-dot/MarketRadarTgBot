from aiogram.fsm.state import State, StatesGroup

class SearchState(StatesGroup):
    waiting_for_crypto = State()
    waiting_for_stock = State()
    waiting_for_metal = State()