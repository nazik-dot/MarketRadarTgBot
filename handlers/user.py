from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.main_kb import *

# ===== СЕРВІСИ =====
from services.crypto_service import find_cryptocurrency
from services.stock_service import find_stock
from services.metal_service import find_precious_metal
from states.alert_state import AlertState
from services.asset_service import get_user_assets
from services.alert_service import add_alert
from services.stock_service import get_stock_price



router = Router()


# =========================================================
# 🟢 ГОЛОВНЕ МЕНЮ
# =========================================================

@router.message(F.text == "/start")
async def start_handler(message: Message):
    """Вітає користувача"""
    await message.answer("Hi! I'm MarketRadarBot. I can help you to track cryptocurrency," \
    " stocks, and precious metals. Use the menu to find assets or manage your portfolio.", reply_markup=main_keyboard)
    return

@router.message(F.text == "💸 Find cryptocurrency")
async def crypto_handler(message: Message):
    """Запитує у користувача назву криптовалюти"""
    await message.answer("Enter the name of the cryptocurrency:")


@router.message(F.text == "📃 Find stock")
async def stock_handler(message: Message):
    """Запитує у користувача назву акції"""
    await message.answer("Enter the name of the stock:")


@router.message(F.text == "💎 Find precious metal")
async def metal_handler(message: Message):
    """Запитує у користувача назву металу"""
    await message.answer("Enter the name of the precious metal (gold, silver, platinum, palladium):")


@router.message(F.text == "🪙 See all my added assets")
async def show_assets_handler(message: Message):
    """Показує всі додані активи користувача"""
    user_id = message.from_user.id
    assets = get_user_assets(user_id)

    if not assets:
        await message.answer("You don't have any added assets yet.")
        return

    text = "\n".join(str(asset) for asset in assets)
    await message.answer(text)


# =========================================================
# 🔵 CALLBACK КНОПКИ
# =========================================================

@router.callback_query(F.data == "assets:list")
async def assets_list(callback: CallbackQuery):
    """Показує список активів через inline кнопку"""
    user_id = callback.from_user.id
    assets = get_user_assets(user_id)

    if not assets:
        await callback.message.answer("No assets found.")
        return

    text = "\n".join(str(asset) for asset in assets)
    await callback.message.answer(text)


@router.callback_query(F.data == "alert:add")
async def alert_add(callback: CallbackQuery):
    """
    Тимчасова заглушка.
    Тут пізніше буде FSM для додавання алерта
    """
    await callback.message.answer(
        "Enter the asset and price (e.g., BTC 50000)"
    )


@router.callback_query(F.data == "assets:delete")
async def asset_delete(callback: CallbackQuery):
    """Запит на видалення активу"""
    await callback.message.answer("Enter the ID of the asset to delete")

# =========================================================
# ALERTS
# =========================================================

@router.message(AlertState.waiting_for_alert)
async def process_alert(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()

    parts = text.split()

    if len(parts) != 3:
        await message.answer("Format: BTC 50000 up/down")
        return

    asset, price_str, direction = parts

    if direction not in ("up", "down"):
        await message.answer("direction needs to be: up or down")
        return

    try:
        price = float(price_str)
    except ValueError:
        await message.answer("Price must be a number.")
        return

    add_alert(
        user_id=message.from_user.id,
        asset_id=asset,
        target_price=price,
        direction=direction
    )

    await message.answer(f"Alert added: {asset} --> {price} ({direction})")

    await state.clear()

# =========================================================
# ⚠️ УНІВЕРСАЛЬНИЙ ПОШУК
# =========================================================

from aiogram.fsm.context import FSMContext

@router.message(F.text)
async def universal_handler(message: Message, state: FSMContext):
    query = (message.text or "").strip().lower()

    if not query:
        await message.answer("Please enter a valid query.")
        return

    if query in ("/start", "start"):
        return


    # ---- КРИПТОВАЛЮТА ----
    crypto = find_cryptocurrency(query)
    if crypto:
        text = "\n".join(
            f"{c['name']} ({c['symbol']})" for c in crypto
        )
        await message.answer(text)
        return


    # ---- АКЦІЇ ----
    stock = await find_stock(query)

    if stock:
        best = stock[0]

        price = await get_stock_price(best["symbol"])

        text = (
            f"{best['name']} ({best['symbol']})\n"
            f"Price: {price}$"
        )

        await message.answer(text)
        return


    # ---- МЕТАЛИ ----
    metal_price = find_precious_metal(query)
    if metal_price:
        await message.answer(f"{query.title()} price: {metal_price}$")
        return


    # ---- НІЧОГО НЕ ЗНАЙДЕНО ----
    await message.answer("Nothing was found 😢")