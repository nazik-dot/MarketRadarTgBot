import requests

BASE_URL = "https://api.coinpaprika.com/v1"


def find_cryptocurrency(query: str):
    try:
        coins = requests.get(f"{BASE_URL}/coins").json()

        results = [
            {
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin["symbol"]
            }
            for coin in coins
            if query.lower() in coin["name"].lower()
        ]

        return results[:5] if results else None

    except Exception as e:
        print(f"[crypto_service] error: {e}")
        return None


def get_crypto_price(coin_id: str):
    try:
        data = requests.get(f"{BASE_URL}/tickers/{coin_id}").json()
        return data.get("quotes", {}).get("USD", {}).get("price")
    except Exception as e:
        print(f"[crypto_service] price error: {e}")
        return None