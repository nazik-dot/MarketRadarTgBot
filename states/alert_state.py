from aiogram.fsm.state import State, StatesGroup

class AlertState(StatesGroup):
    waiting_for_alert = State()