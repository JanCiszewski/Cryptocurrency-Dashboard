from fastapi import APIRouter, HTTPException
from app.services import crypto_service
from app.schemas.coin import CoinResponse
from typing import List

router = APIRouter(
    prefix="/coins",
    tags=["Kryptowaluty"]
)

@router.get("/", response_model=List[CoinResponse])
async def get_all_coins():
    data = crypto_service.get_coins()
    if not data:
        raise HTTPException(status_code=503, detail="Błąd pobierania danych z API")
    return data

@router.get("/{coin_id}", response_model=CoinResponse)
async def get_single_coin(coin_id: str):
    data = crypto_service.get_coin(coin_id)
    if not data or "error" in data:
        detail = data.get("error", "Coin not found") if isinstance(data, dict) else "Coin not found"
        raise HTTPException(status_code=404, detail=detail)
    return data