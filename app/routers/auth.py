from fastapi import APIRouter
from pydantic import BaseModel

# Tworzymy router dla sekcji autoryzacji
router = APIRouter(prefix="/auth", tags=["Autoryzacja"])

# Model danych - czego oczekujemy od użytkownika przy logowaniu
class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(data: LoginData):
    # MOCK: Sztuczny token. Auth Guy podmieni to potem na prawdziwe JWT.
    return {"access_token": "fake-super-secret-token", "token_type": "bearer"}

@router.get("/me")
async def get_current_user():
    # MOCK: Zwracamy sztuczne dane rzekomo zalogowanego użytkownika
    return {"id": 1, "username": "alan_tester", "email": "alan@example.com"}