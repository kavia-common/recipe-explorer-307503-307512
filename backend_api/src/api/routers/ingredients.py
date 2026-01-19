"""
Ingredients router: search recipes by included ingredients.
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from src.api.data import RECIPES
from src.api.schemas import PaginatedResponse, Recipe
from src.api.utils import paginate, recipe_matches_include_all, sort_recipes

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


# PUBLIC_INTERFACE
@router.get(
    "/search",
    response_model=PaginatedResponse[Recipe],
    summary="Search recipes by ingredients",
    description="Search recipes that include all ingredient tokens in ?include=comma,separated form.",
    operation_id="search_recipes_by_ingredients",
)
def search_by_ingredients(
    include: str = Query(..., description="Comma-separated ingredient tokens; recipe must include ALL"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    sort: str = Query("rating", description="Sort by 'rating' or 'title'"),
):
    """Return recipes matching include-all ingredients."""
    filtered = [r for r in RECIPES if recipe_matches_include_all(r, include)]
    filtered = sort_recipes(filtered, sort)
    return paginate(filtered, page, limit)
