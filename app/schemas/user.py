from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CoinHolding(BaseModel):
    id: str
    amount: float

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    balance: float
    coins: List[CoinHolding]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str