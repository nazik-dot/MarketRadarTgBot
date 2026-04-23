from aiogram.fsm.state import State, StatesGroup

class AlertState(StatesGroup):
    waiting_for_alert = State()
    waiting_for_delete_alert = State()
    waiting_for_add_asset = State()