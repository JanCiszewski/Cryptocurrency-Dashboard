from fastapi import FastAPI
from app.routers import coins, auth, demo
from app.routers import coins, auth, demo, favorites
from app.routers import coins, auth, demo, favorites, payments

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crypto Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coins.router)
app.include_router(auth.router)
app.include_router(demo.router)
app.include_router(favorites.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "API działa! Przejdź do /docs aby zobaczyć Swaggera."}