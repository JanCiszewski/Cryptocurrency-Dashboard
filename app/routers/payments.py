from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/payments",
    tags=["Płatności"]
)

@router.post("/create")
async def create_payment(amount: float):
    return {
        "status": "success",
        "redirect_url": "https://merch-prod.snd.payu.com/...",
        "order_id": "987654321"
    }

@router.post("/webhook")
async def payu_webhook(data: dict):
    return {"status": "received"}