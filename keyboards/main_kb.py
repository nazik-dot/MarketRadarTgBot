from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="💸 Find cryptocurrency")],
        [KeyboardButton(text="📃 Find stock")],
        [KeyboardButton(text="💎 Find precious metal")],
        [KeyboardButton(text="🪙 More options")]
    ],
    resize_keyboard=True
)

more_options_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="🔔 Add alert")],
        [KeyboardButton(text="🗑️ Delete alert")],
        [KeyboardButton(text="📋 My alerts")],
        [KeyboardButton(text="🔙 Back to main menu")]
    ],
    resize_keyboard=True
)