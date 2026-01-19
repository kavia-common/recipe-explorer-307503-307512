"""
Favorites router: CRUD favorites for a mock user id.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.api.data import FAVORITES_BY_USER, MOCK_USER_ID, RECIPES
from src.api.schemas import Favorite, FavoriteCreateRequest

router = APIRouter(prefix="/favorites", tags=["favorites"])


def _recipe_exists(recipe_id: int) -> bool:
    return any(int(r["id"]) == int(recipe_id) for r in RECIPES)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=list[Favorite],
    summary="List favorites",
    description="List favorite recipes for the mock user id.",
    operation_id="list_favorites",
)
def list_favorites(user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Return favorites for a user."""
    ids = FAVORITES_BY_USER.get(user_id, [])
    return [{"user_id": user_id, "recipe_id": rid} for rid in ids]


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Favorite,
    summary="Add favorite",
    description="Add a recipe to favorites for the mock user id.",
    operation_id="add_favorite",
)
def add_favorite(payload: FavoriteCreateRequest, user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Add a favorite for a user."""
    if not _recipe_exists(payload.recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")

    FAVORITES_BY_USER.setdefault(user_id, [])
    if payload.recipe_id not in FAVORITES_BY_USER[user_id]:
        FAVORITES_BY_USER[user_id].append(payload.recipe_id)
    return {"user_id": user_id, "recipe_id": payload.recipe_id}


# PUBLIC_INTERFACE
@router.delete(
    "/{recipe_id}",
    response_model=dict,
    summary="Remove favorite",
    description="Remove a recipe from favorites for the mock user id.",
    operation_id="remove_favorite",
)
def remove_favorite(recipe_id: int, user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Remove a favorite for a user."""
    ids = FAVORITES_BY_USER.get(user_id, [])
    if recipe_id in ids:
        FAVORITES_BY_USER[user_id] = [rid for rid in ids if int(rid) != int(recipe_id)]
    return {"ok": True}
