from aiogram.fsm.state import State, StatesGroup

class AlertState(StatesGroup):
    choosing_asset = State()
    choosing_price = State()
    confirming = State()