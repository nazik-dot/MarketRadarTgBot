from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main_kb import *

# ===== СЕРВІСИ =====
from services.crypto_service import find_cryptocurrency, get_crypto_price
from services.stock_service import find_stock, get_stock_price
from services.metal_service import find_precious_metal
from services.asset_service import get_user_assets, add_asset, delete_asset
from services.alert_service import add_alert, get_user_alerts, delete_alert

# ===== СТАНИ =====
from states.alert_state import AlertState
from states.search_state import SearchState

router = Router()


# =========================================================
# 🟢 ГОЛОВНЕ МЕНЮ
# =========================================================

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    """Вітає користувача та скидає стани"""
    await state.clear()
    await message.answer(
        "Hi! I'm MarketRadarBot. I can help you to track cryptocurrency, "
        "stocks, and precious metals. Use the menu to find assets or manage your portfolio.",
        reply_markup=main_keyboard
    )


@router.message(F.text.startswith("/add"))
async def add_asset_handler(message: Message, state: FSMContext):
    """Додає актив до портфоліо користувача"""
    text = message.text.strip()
    parts = text.split()
    
    if len(parts) < 2:
        await message.answer("Usage: /add <symbol>\nExample: /add BTC")
        return
    
    symbol = parts[1].upper()
    user_id = message.from_user.id
    
    # Try to get price for the asset
    price = None
    asset_type = "unknown"
    
    # Try crypto price
    try:
        price = await get_crypto_price(symbol.lower())
        if price:
            asset_type = "crypto"
    except:
        pass
    
    # Try stock price if not found
    if not price:
        try:
            price = await get_stock_price(symbol)
            if price and price != "Error (Check ticker)" and price != "Limit reached":
                asset_type = "stock"
        except:
            pass
    
    # Try metal price if not found
    if not price:
        metal_price = find_precious_metal(symbol.lower())
        if metal_price:
            price = metal_price
            asset_type = "metal"
    
    if price:
        asset = {
            "id": symbol,
            "type": asset_type,
            "price": price
        }
        add_asset(user_id, asset)
        await message.answer(f"✅ Added {symbol} ({asset_type}) - ${price}")
    else:
        await message.answer(f"❌ Could not find price for {symbol}. Try searching first.")


@router.message(F.text.startswith("/delete"))
async def delete_asset_handler(message: Message, state: FSMContext):
    """Видаляє актив з портфоліо користувача"""
    text = message.text.strip()
    parts = text.split()
    
    if len(parts) < 2:
        await message.answer("Usage: /delete <symbol>\nExample: /delete BTC")
        return
    
    symbol = parts[1].upper()
    user_id = message.from_user.id
    
    # Get current assets to check if exists
    assets = get_user_assets(user_id)
    asset_exists = any(a.get("id") == symbol for a in assets)
    
    if not asset_exists:
        await message.answer(f"❌ Asset {symbol} not found in your portfolio.")
        return
    
    delete_asset(user_id, symbol)
    await message.answer(f"✅ Deleted {symbol} from your portfolio.")


@router.message(F.text == "💸 Find cryptocurrency")
async def crypto_handler(message: Message, state: FSMContext):
    """Запитує у користувача назву криптовалюти"""
    await message.answer("Enter the name or symbol of the cryptocurrency (e.g. Bitcoin or BTC):")
    await state.set_state(SearchState.waiting_for_crypto)


@router.message(F.text == "📃 Find stock")
async def stock_handler(message: Message, state: FSMContext):
    """Запитує у користувача назву акції"""
    await message.answer("Enter the name or ticker of the stock (e.g. Apple or AAPL):")
    await state.set_state(SearchState.waiting_for_stock)


@router.message(F.text == "💎 Find precious metal")
async def metal_handler(message: Message, state: FSMContext):
    """Запитує у користувача назву металу"""
    await message.answer("Enter the name of the precious metal (gold, silver, platinum, palladium):")
    await state.set_state(SearchState.waiting_for_metal)


@router.message(F.text == "🪙 More options")
async def more_options_handler(message: Message, state: FSMContext):
    """Показує меню додаткових опцій"""
    await state.clear()
    await message.answer(
        "Choose an option:",
        reply_markup=more_options_keyboard
    )


@router.message(F.text == "🔙 Back to main menu")
async def back_to_main_handler(message: Message, state: FSMContext):
    """Повертає до головного меню"""
    await state.clear()
    await message.answer(
        "Back to main menu:",
        reply_markup=main_keyboard
    )


@router.message(F.text == "🔔 Add alert")
async def add_alert_handler(message: Message, state: FSMContext):
    """Запускає процес додавання алерта"""
    await message.answer(
        "Enter the asset name, target price and direction (up/down).\n"
        "Format: BTC 50000 up"
    )
    await state.set_state(AlertState.waiting_for_alert)


@router.message(F.text == "🗑️ Delete alert")
async def delete_alert_handler(message: Message, state: FSMContext):
    """Показує список алертів для видалення"""
    user_id = message.from_user.id
    alerts = get_user_alerts(user_id)

    if not alerts:
        await message.answer("You don't have any alerts to delete.")
        return

    text = "Your alerts (send the number to delete):\n\n"
    for i, alert in enumerate(alerts):
        text += f"{i+1}. {alert['asset_id']} - {alert['target_price']} ({alert['direction']})\n"
    
    text += "\nSend the number of the alert to delete."
    await message.answer(text)
    await state.set_state(AlertState.waiting_for_delete_alert)


@router.message(F.text == "📋 My alerts")
async def my_alerts_handler(message: Message):
    """Показує всі алерти користувача"""
    user_id = message.from_user.id
    alerts = get_user_alerts(user_id)

    if not alerts:
        await message.answer("You don't have any alerts set.")
        return

    text = "Your alerts:\n\n"
    for i, alert in enumerate(alerts):
        text += f"{i+1}. {alert['asset_id']} - {alert['target_price']} ({alert['direction']})\n"
    
    await message.answer(text)


@router.message(F.text == "📁 My assets")
async def show_assets_handler(message: Message):
    """Показує всі додані активи користувача"""
    user_id = message.from_user.id
    assets = get_user_assets(user_id)

    if not assets:
        await message.answer("You don't have any added assets yet.")
        return

    text = "Your assets:\n" + "\n".join(str(asset) for asset in assets)
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

    text = "Your assets:\n" + "\n".join(str(asset) for asset in assets)
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "alert:add")
async def alert_add_callback(callback: CallbackQuery, state: FSMContext):
    """Запускає процес додавання алерта"""
    await callback.message.answer(
        "Enter the asset name, target price and direction (up/down).\n"
        "Format: BTC 50000 up"
    )
    await state.set_state(AlertState.waiting_for_alert)
    await callback.answer()


@router.callback_query(F.data == "alert:delete")
async def alert_delete_callback(callback: CallbackQuery, state: FSMContext):
    """Показує список алертів для видалення через callback"""
    user_id = callback.from_user.id
    alerts = get_user_alerts(user_id)

    if not alerts:
        await callback.message.answer("You don't have any alerts to delete.")
        await callback.answer()
        return

    text = "Your alerts (send the number to delete):\n\n"
    for i, alert in enumerate(alerts):
        text += f"{i+1}. {alert['asset_id']} - {alert['target_price']} ({alert['direction']})\n"
    
    text += "\nSend the number of the alert to delete."
    await callback.message.answer(text)
    await state.set_state(AlertState.waiting_for_delete_alert)
    await callback.answer()


@router.callback_query(F.data == "alert:list")
async def alert_list_callback(callback: CallbackQuery):
    """Показує список алертів через callback"""
    user_id = callback.from_user.id
    alerts = get_user_alerts(user_id)

    if not alerts:
        await callback.message.answer("You don't have any alerts set.")
        await callback.answer()
        return

    text = "Your alerts:\n\n"
    for i, alert in enumerate(alerts):
        text += f"{i+1}. {alert['asset_id']} - {alert['target_price']} ({alert['direction']})\n"
    
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "assets:delete")
async def asset_delete_callback(callback: CallbackQuery):
    """Запит на видалення активу"""
    await callback.message.answer("Please enter the ID of the asset to delete (This feature is coming soon).")
    await callback.answer()


# =========================================================
# 🔍 ОБРОБКА ПОШУКУ (FSM)
# =========================================================

@router.message(SearchState.waiting_for_crypto)
async def process_crypto_search(message: Message, state: FSMContext):
    query = message.text.strip()
    crypto_list = await find_cryptocurrency(query)

    if crypto_list:
        text = "Found cryptocurrencies:\n"
        for c in crypto_list:
            price = await get_crypto_price(c['id'])
            price_text = f" - ${price}" if price else ""
            text += f"• {c['name']} ({c['symbol']}){price_text}\n"
        
        text += "\nTo add an asset, use: /add BTC (symbol)"
        await message.answer(text)
        
        # Store found assets in state for adding
        await state.update_data(found_cryptos=crypto_list)
    else:
        await message.answer(f"No cryptocurrency found for '{query}'.")
    
    await state.clear()


@router.message(SearchState.waiting_for_stock)
async def process_stock_search(message: Message, state: FSMContext):
    query = message.text.strip()
    stocks = await find_stock(query)

    if stocks == "Limit":
        await message.answer("⚠️ API rate limit reached. Please wait a minute and try again.")
        await state.clear()
        return

    if stocks:
        await message.answer(f"Searching prices for {len(stocks)} symbols...")
        text = "🔍 Found stocks:\n\n"
        
        for s in stocks:
            price = await get_stock_price(s['symbol'])
            
            if price == "Limit reached":
                price_text = " - (Rate limit reached)"
            elif price == "Error (Check ticker)":
                price_text = " - (Price unavailable)"
            elif price:
                price_text = f" - **${price}**"
            else:
                price_text = " - (Price not found)"
            
            text += f"• {s['name']} (`{s['symbol']}`){price_text}\n"
        
        text += "\nTo add an asset, use: /add AAPL (symbol)"
        await message.answer(text, parse_mode="Markdown")
        
        # Store found stocks in state for adding
        await state.update_data(found_stocks=stocks)
    else:
        await message.answer(f"❌ No stocks found for '{query}'.")
    
    await state.clear()


@router.message(SearchState.waiting_for_metal)
async def process_metal_search(message: Message, state: FSMContext):
    query = message.text.strip().lower()
    price = find_precious_metal(query)

    if price:
        await message.answer(f"Current {query.title()} price: ${price} per oz\n\nTo add this metal, use: /add gold")
        
        # Store found metal in state for adding
        await state.update_data(found_metal={"name": query.title(), "price": price})
    else:
        await message.answer(f"Unknown metal '{query}'. Try gold, silver, platinum, or palladium.")
    
    await state.clear()


# =========================================================
# 🔔 ALERTS (FSM)
# =========================================================

@router.message(AlertState.waiting_for_alert)
async def process_alert(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    parts = text.split()

    if len(parts) != 3:
        await message.answer("Invalid format. Use: BTC 50000 up")
        return

    asset, price_str, direction = parts

    if direction not in ("up", "down"):
        await message.answer("Direction must be 'up' or 'down'.")
        return

    try:
        price = float(price_str)
    except ValueError:
        await message.answer("Price must be a valid number.")
        return

    add_alert(
        user_id=message.from_user.id,
        asset_id=asset.upper(),
        target_price=price,
        direction=direction
    )

    await message.answer(f"✅ Alert set: {asset.upper()} {direction} to {price}")
    await state.clear()


@router.message(AlertState.waiting_for_delete_alert)
async def process_delete_alert(message: Message, state: FSMContext):
    """Обробляє видалення алерта"""
    text = (message.text or "").strip()
    
    try:
        alert_index = int(text) - 1  # Конвертуємо в індекс (0-based)
    except ValueError:
        await message.answer("Please send a valid number.")
        return

    user_id = message.from_user.id
    success = delete_alert(user_id, alert_index)

    if success:
        await message.answer("✅ Alert deleted successfully!")
    else:
        await message.answer("❌ Alert not found. Please check the number.")
    
    await state.clear()


# =========================================================
# ⚠️ УНІВЕРСАЛЬНИЙ ОБРОБНИК (Fallback)
# =========================================================

@router.message(F.text)
async def universal_handler(message: Message):
    """Обробляє текст, який не потрапив у FSM"""
    if message.text.startswith("/"):
        return # Ignore unknown commands
        
    await message.answer(
        "I'm not sure what you mean. Please use the menu buttons to start a search.",
        reply_markup=main_keyboard
    )