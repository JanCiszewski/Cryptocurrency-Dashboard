from pydantic import BaseModel

class CoinResponse(BaseModel):
    id: str
    name: str
    symbol: str
    price: float