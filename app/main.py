from fastapi import FastAPI
from app.routers import coins, auth, demo # Dodaliśmy tu auth i demo

from fastapi.middleware.cors import CORSMiddleware #potrzebne do fetchowania API we frontendzie

app = FastAPI(title="Crypto Dashboard API")

#usuwanie błędu CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Podpinamy wszystkie Twoje routery
app.include_router(coins.router)
app.include_router(auth.router)   # Nowe
app.include_router(demo.router)   # Nowe

@app.get("/")
async def root():
    return {"message": "API działa! Przejdź do /docs aby zobaczyć Swaggera."}