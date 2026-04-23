import aiohttp
import time

BASE_URL = "https://api.coinpaprika.com/v1"

# Простий кеш для списку монет
_COINS_CACHE = []
_LAST_FETCH_TIME = 0
CACHE_TTL = 3600  # 1 година

async def _get_all_coins():
    global _COINS_CACHE, _LAST_FETCH_TIME
    
    current_time = time.time()
    if _COINS_CACHE and (current_time - _LAST_FETCH_TIME < CACHE_TTL):
        return _COINS_CACHE
        
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/coins", timeout=10) as resp:
                _COINS_CACHE = await resp.json()
                _LAST_FETCH_TIME = current_time
        return _COINS_CACHE
    except Exception as e:
        print(f"[crypto_service] fetch all coins error: {e}")
        return _COINS_CACHE or []

async def find_cryptocurrency(query: str):
    try:
        coins = await _get_all_coins()
        query = query.lower()

        results = [
            {
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin["symbol"]
            }
            for coin in coins
            if query in coin["name"].lower() or query in coin["symbol"].lower()
        ]

        return results[:5] if results else None

    except Exception as e:
        print(f"[crypto_service] error: {e}")
        return None

async def get_crypto_price(coin_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/tickers/{coin_id}", timeout=10) as resp:
                data = await resp.json()
        
        price = data.get("quotes", {}).get("USD", {}).get("price")
        if price:
            return f"{float(price):.2f}"
        return None
    except Exception as e:
        print(f"[crypto_service] price error: {e}")
        return None