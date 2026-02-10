from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pathlib import Path
import json

router = APIRouter(prefix="/cards", tags=["cards"])

DATA_DIR = Path("data")  # Folder containing shop JSON files

@router.get("/")
def get_cards(shop_id: str = Query(...), card_ids: Optional[List[int]] = Query(None)):
    """
    Fetch Bingo cards by shop_id. Optionally filter by card_ids.
    """
    json_file = DATA_DIR / f"{shop_id}.json"
    if not json_file.exists():
        raise HTTPException(status_code=404, detail=f"No file for shop_id '{shop_id}'")

    with open(json_file, "r") as f:
        cards_data = json.load(f)

    if card_ids:
        cards_data = [card for card in cards_data if card["card_id"] in card_ids]

    if not cards_data:
        raise HTTPException(status_code=404, detail="No cards found")

    return cards_data
