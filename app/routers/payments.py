from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(
    prefix="/payments",
    tags=["Płatności"]
)

class PaymentCreate(BaseModel):
    amount_in_cents: int

@router.post("")
async def create_payment(payment_data: PaymentCreate):
    client_id = "460718"
    client_secret = "22f4175da9f0f72bcce976dd8bd7504f"
    
    async with httpx.AsyncClient() as client:
        auth_response = await client.post(
            "https://secure.payu.com/pl/standard/user/oauth/authorize",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            }
        )
        
        if auth_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Błąd uwierzytelniania PayU")
            
        token_data = auth_response.json()
        access_token = token_data["access_token"]
        
        order_payload = {
            "customerIp": "127.0.0.1",
            "merchantPosId": "145227",
            "description": "Zakupy w aplikacji",
            "currencyCode": "PLN",
            "totalAmount": str(payment_data.amount_in_cents),
            "products": [
                {
                    "name": "Transakcja online",
                    "unitPrice": str(payment_data.amount_in_cents),
                    "quantity": "1"
                }
            ]
        }
        
        order_response = await client.post(
            "https://secure.payu.com/api/v2_1/orders",
            json=order_payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            follow_redirects=False
        )
        
        if order_response.status_code not in [200, 201, 302]:
            raise HTTPException(status_code=400, detail="Błąd tworzenia zamówienia PayU")
            
        order_data = order_response.json()
        
        return {
            "status": "success",
            "redirect_url": order_data["redirectUri"],
            "order_id": order_data["orderId"]
        }

@router.post("/webhook")
async def payu_webhook(data: dict):
    return {"status": "received"}