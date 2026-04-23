import aiohttp
import os

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

async def get_stock_price(symbol: str):
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()

        return data.get("Global Quote", {}).get("05. price")

    except Exception as e:
        print(f"[stock_service] price error: {e}")
        return None


async def find_stock(query: str):
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=SYMBOL_SEARCH&keywords={query}&apikey={API_KEY}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()

        matches = data.get("bestMatches", []) or []

        return [
            {
                "symbol": m.get("1. symbol"),
                "name": m.get("2. name")
            }
            for m in matches[:5]
            if m.get("1. symbol") and m.get("2. name")
        ]

    except Exception as e:
        print(f"[stock_service] error: {e}")
        return []
    
async def get_stock_price(symbol: str):
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()

        return data.get("Global Quote", {}).get("05. price")

    except Exception as e:
        print(f"[stock_service] price error: {e}")
        return None