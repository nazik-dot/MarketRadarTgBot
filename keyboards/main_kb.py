from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="💸 Find cryptocurrency")],
        [KeyboardButton(text="📃 Find stock")],
        [KeyboardButton(text="💎 Find precious metal")],
        [KeyboardButton(text="🪙 See all my added assets")]
    ], resize_keyboard=True
)