import requests

BASE_URL = "https://api.coingecko.com/api/v3"

def get_coins():
    try:
        response = requests.get(
            f"{BASE_URL}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        coins = []

        for coin in data:
            coins.append({
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin["symbol"],
                "price": coin["current_price"]
            })

        return coins

    except requests.exceptions.RequestException as error:
        print(f"Błąd podczas pobierania listy kryptowalut: {error}")
        return []

def get_coin(coin_id):
    try:
        response = requests.get(
            f"{BASE_URL}/coins/{coin_id}",
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        coin = {
            "id": data["id"],
            "name": data["name"],
            "symbol": data["symbol"],
            "price": data["market_data"]["current_price"]["usd"]
        }

        return coin

    except requests.exceptions.RequestException as error:
        print(f"Błąd podczas pobierania kryptowaluty '{coin_id}': {error}")
        return {"error": "Coin not found"}
