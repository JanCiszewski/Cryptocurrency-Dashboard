from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/favorites", tags=["Ulubione"])

@router.get("/")
async def get_favorites():
    return []

@router.post("/{coin_id}")
async def add_favorite(coin_id: str):
    return {"message": f"Dodano {coin_id} do ulubionych"}

@router.put("/{coin_id}")
async def update_favorite_note(coin_id: str, note: str):
    return {"message": f"Zaktualizowano notatkę dla {coin_id}", "note": note}

@router.delete("/{coin_id}")
async def delete_favorite(coin_id: str):
    return {"message": f"Usunięto {coin_id} z ulubionych"}