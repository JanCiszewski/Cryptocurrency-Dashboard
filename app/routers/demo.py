from fastapi import APIRouter


router = APIRouter(prefix="/demo", tags=["Demo Portfolio"])

@router.get("/portfolio")
async def get_portfolio():
    return {
        "portfolio_total_value": 325.50,
        "items": [
            {"coin_id": "bitcoin", "total_coin_amount": 0.005, "current_price": 64000}
        ]
    }