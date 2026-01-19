"""
Recipes router: list, detail, create placeholder, and search/filter endpoints.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from src.api.data import RECIPES
from src.api.schemas import PaginatedResponse, Recipe, RecipeCreatePlaceholderRequest
from src.api.utils import paginate, recipe_matches_category, recipe_matches_ingredients_or, recipe_matches_query, sort_recipes

router = APIRouter(prefix="/recipes", tags=["recipes"])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=PaginatedResponse[Recipe],
    summary="List recipes",
    description="List recipes with pagination and optional filtering by query, category, and ingredients.",
    operation_id="list_recipes",
)
def list_recipes(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    q: Optional[str] = Query(None, description="Search in title/description"),
    category: Optional[str] = Query(None, description="Filter by category"),
    ingredients: Optional[str] = Query(None, description="Comma-separated ingredient tokens (OR match)"),
    sort: Optional[str] = Query("rating", description="Sort by 'rating' or 'title'"),
):
    """
    List recipes.

    Filtering:
    - q: substring match against title/description (case-insensitive)
    - category: exact match (case-insensitive)
    - ingredients: OR-match against ingredient names (case-insensitive substring)

    Sorting:
    - rating: rating_avg desc, then rating_count desc
    - title: title asc
    """
    filtered = []
    for r in RECIPES:
        if q and not recipe_matches_query(r, q):
            continue
        if category and not recipe_matches_category(r, category):
            continue
        if ingredients and not recipe_matches_ingredients_or(r, ingredients):
            continue
        filtered.append(r)

    filtered = sort_recipes(filtered, sort or "rating")
    return paginate(filtered, page, limit)


# PUBLIC_INTERFACE
@router.get(
    "/{recipe_id}",
    response_model=Recipe,
    summary="Get recipe detail",
    description="Get recipe by id.",
    operation_id="get_recipe",
)
def get_recipe(recipe_id: int):
    """Return a single recipe by id."""
    for r in RECIPES:
        if int(r["id"]) == int(recipe_id):
            return r
    return {"detail": "Recipe not found"}


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Recipe,
    summary="Create recipe (placeholder)",
    description="Create a recipe placeholder. In this in-memory version, the recipe is returned but not persisted.",
    operation_id="create_recipe_placeholder",
)
def create_recipe_placeholder(payload: RecipeCreatePlaceholderRequest):
    """
    Placeholder create endpoint.

    Returns a new recipe object with a generated id, but does not persist to storage.
    """
    next_id = max([r["id"] for r in RECIPES], default=0) + 1
    created = {
        "id": next_id,
        "title": payload.title,
        "description": payload.description,
        "category": payload.category,
        "ingredients": [i.model_dump() for i in payload.ingredients],
        "steps": payload.steps,
        "image": payload.image or "https://picsum.photos/seed/new-recipe/600/400",
        "rating_avg": 0.0,
        "rating_count": 0,
    }
    return created
