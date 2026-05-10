from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Autoryzacja"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Mock odpowiedzi - tu Auth Guy wepnie bazę danych
    return {"id": 1, "username": user.username, "role": "user"}

@router.post("/login", response_model=TokenResponse)
async def login(user: UserCreate):
    # Mock odpowiedzi - tu Auth Guy wepnie generowanie JWT
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me():
    return {"id": 1, "username": "alan_tester", "role": "admin"}