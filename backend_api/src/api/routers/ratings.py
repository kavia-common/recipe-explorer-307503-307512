"""
Ratings router: CRUD ratings for a mock user id.

This implementation stores per-user ratings in-memory and updates each recipe's
rating_avg and rating_count.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.api.data import MOCK_USER_ID, RATINGS_BY_USER, RECIPES
from src.api.schemas import Rating, RatingUpsertRequest

router = APIRouter(prefix="/ratings", tags=["ratings"])


def _find_recipe(recipe_id: int):
    for r in RECIPES:
        if int(r["id"]) == int(recipe_id):
            return r
    return None


def _recompute_recipe_aggregate(recipe_id: int):
    """Recompute recipe rating_avg and rating_count from all users."""
    all_ratings = []
    for _uid, mapping in RATINGS_BY_USER.items():
        if recipe_id in mapping:
            all_ratings.append(mapping[recipe_id])

    recipe = _find_recipe(recipe_id)
    if not recipe:
        return

    if not all_ratings:
        recipe["rating_avg"] = 0.0
        recipe["rating_count"] = 0
        return

    recipe["rating_count"] = len(all_ratings)
    recipe["rating_avg"] = round(sum(all_ratings) / len(all_ratings), 2)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=list[Rating],
    summary="List ratings by user",
    description="List all ratings for the mock user id.",
    operation_id="list_ratings",
)
def list_ratings(user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Return user ratings."""
    mapping = RATINGS_BY_USER.get(user_id, {})
    return [{"user_id": user_id, "recipe_id": rid, "rating": val} for rid, val in mapping.items()]


# PUBLIC_INTERFACE
@router.get(
    "/{recipe_id}",
    response_model=Rating,
    summary="Get rating by recipe",
    description="Get the user's rating for a recipe.",
    operation_id="get_rating",
)
def get_rating(recipe_id: int, user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Return user's rating for recipe."""
    if not _find_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")

    mapping = RATINGS_BY_USER.get(user_id, {})
    if recipe_id not in mapping:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"user_id": user_id, "recipe_id": recipe_id, "rating": mapping[recipe_id]}


# PUBLIC_INTERFACE
@router.put(
    "/{recipe_id}",
    response_model=Rating,
    summary="Upsert rating",
    description="Set/update the user's rating for a recipe (1-5). Updates recipe aggregates.",
    operation_id="upsert_rating",
)
def upsert_rating(
    recipe_id: int,
    payload: RatingUpsertRequest,
    user_id: str = Query(MOCK_USER_ID, description="Mock user id"),
):
    """Upsert a rating."""
    if not _find_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")

    RATINGS_BY_USER.setdefault(user_id, {})
    RATINGS_BY_USER[user_id][recipe_id] = payload.rating
    _recompute_recipe_aggregate(recipe_id)
    return {"user_id": user_id, "recipe_id": recipe_id, "rating": payload.rating}


# PUBLIC_INTERFACE
@router.delete(
    "/{recipe_id}",
    response_model=dict,
    summary="Delete rating",
    description="Delete the user's rating for a recipe. Updates recipe aggregates.",
    operation_id="delete_rating",
)
def delete_rating(recipe_id: int, user_id: str = Query(MOCK_USER_ID, description="Mock user id")):
    """Delete a rating."""
    if not _find_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")

    mapping = RATINGS_BY_USER.get(user_id, {})
    if recipe_id in mapping:
        del mapping[recipe_id]
        RATINGS_BY_USER[user_id] = mapping
        _recompute_recipe_aggregate(recipe_id)
    return {"ok": True}
