from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserUpdate
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    oauth2_scheme
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
import json


router = APIRouter(prefix="/auth", tags=["Auth"])

# ======================
# REGISTER
# ======================
@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # sprawdzenie czy email istnieje
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        balance=0,
        coins="[]"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "balance": new_user.balance,
        "coins": []
    }

# ======================
# LOGIN
# ======================
@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ======================
# ME (protected)
# ======================
@router.get("/me", response_model=UserResponse)
async def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "balance": user.balance,
        "coins": json.loads(user.coins)
    }

# ======================
# UPDATE USER
# ======================
@router.put("/update")
async def update_user(
    user_data: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.username = user_data.username
    user.email = user_data.email
    if user_data.password.strip() != "":
        user.password = hash_password(
        user_data.password
    )

    db.commit()

    return {
        "message": "Account updated"
    }