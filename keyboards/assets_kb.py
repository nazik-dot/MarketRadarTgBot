from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Callbacks:
    ADD_ALERT = "alert:add"
    DELETE_ALERT = "alert:delete"
    LIST_ASSETS = "assets:list"

def assets_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏰ Add alert", callback_data=Callbacks.ADD_ALERT)],
            [
                InlineKeyboardButton(text="📊 My assets", callback_data=Callbacks.LIST_ASSETS),
                InlineKeyboardButton(text="❌ Delete", callback_data=Callbacks.DELETE_ALERT)
            ]
        ]
    )