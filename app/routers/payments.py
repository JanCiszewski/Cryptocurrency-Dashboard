from fastapi import APIRouter, HTTPException
from app.services.payu_service import create_payment

router = APIRouter(
    prefix="/payments",
    tags=["Płatności"]
)

@router.post("/create")
async def create_payment_route(amount: float):

    amount_in_cents = int(amount * 100)

    result = create_payment(
        total_amount=amount_in_cents,

        description="Crypto purchase",

        buyer_email="test@test.pl",

        continue_url="http://127.0.0.1:5500",

        notify_url="http://127.0.0.1:8000/payments/webhook",

        customer_ip="127.0.0.1"
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return {
        "status": "success",
        "redirect_url": result["redirect_uri"],
        "order_id": result["order_id"]
    }

@router.post("/webhook")
async def payu_webhook(data: dict):

    return {
        "status": "received"
    }