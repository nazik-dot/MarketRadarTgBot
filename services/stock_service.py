import aiohttp
from config import ALPHA_VANTAGE_KEY

async def get_stock_price(symbol: str):
    if not ALPHA_VANTAGE_KEY:
        return None
        
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()

        # Handle various rate limit messages or errors
        if "Note" in data:
            return "Limit reached"
        if "Information" in data:
            return "Limit reached"
        if "Error Message" in data:
            return "Error (Check ticker)"

        quote = data.get("Global Quote", {})
        if not quote:
            return None
            
        price = quote.get("05. price")
        if price:
            # Format price to be cleaner (2 decimals)
            try:
                return f"{float(price):.2f}"
            except:
                return price
        return None

    except Exception as e:
        print(f"[stock_service] price error: {e}")
        return None

async def find_stock(query: str):
    if not ALPHA_VANTAGE_KEY:
        return []
        
    try:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_KEY}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()

        if "Note" in data or "Information" in data:
            return "Limit"

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