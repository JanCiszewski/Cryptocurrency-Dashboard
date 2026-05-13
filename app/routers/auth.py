from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    oauth2_scheme
)

fake_users_db = []

router = APIRouter(prefix="/auth", tags=["Auth"])

# ======================
# REGISTER
# ======================
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):

    for u in fake_users_db:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="User already exists")

    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    }

    fake_users_db.append(new_user)

    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"]
    }


# ======================
# LOGIN
# ======================
@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = None

    for u in fake_users_db:
        if u["email"] == form_data.username:
            db_user = u
            break

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user["email"]}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ======================
# ME (protected)
# ======================
@router.get("/me", response_model=UserResponse)
async def get_me(token: str = Depends(oauth2_scheme)):

    email = verify_token(token)

    for user in fake_users_db:
        if user["email"] == email:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }

    raise HTTPException(status_code=404, detail="User not found")