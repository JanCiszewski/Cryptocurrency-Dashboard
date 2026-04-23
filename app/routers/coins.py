from fastapi import APIRouter

router = APIRouter(
    prefix="/coins",
    tags=["Kryptowaluty"]
)

@router.get("/")
async def get_all_coins():
    # MOCK: Tymczasowe dane dla Frontendu
    return [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "price": 64000, "currency": "usd"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "price": 3200, "currency": "usd"}
    ]

@router.get("/{coin_id}")
async def get_single_coin(coin_id: str):
    # MOCK: Zwracamy sztuczne dane dla jednego coina
    return {"id": coin_id, "symbol": coin_id[:3], "name": coin_id.capitalize(), "price": 1000, "currency": "usd"}

