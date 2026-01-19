"""
Categories router: list categories and list recipes by category.
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from src.api.data import CATEGORIES, RECIPES
from src.api.schemas import Category, PaginatedResponse, Recipe
from src.api.utils import paginate, recipe_matches_category, sort_recipes

router = APIRouter(prefix="/categories", tags=["categories"])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=list[Category],
    summary="List categories",
    description="Return all available recipe categories.",
    operation_id="list_categories",
)
def list_categories():
    """Return all categories."""
    return CATEGORIES


# PUBLIC_INTERFACE
@router.get(
    "/{category_name}/recipes",
    response_model=PaginatedResponse[Recipe],
    summary="List recipes by category",
    description="List recipes for a category with pagination.",
    operation_id="list_recipes_by_category",
)
def list_recipes_by_category(
    category_name: str,
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    sort: str = Query("rating", description="Sort by 'rating' or 'title'"),
):
    """Return recipes in a category."""
    filtered = [r for r in RECIPES if recipe_matches_category(r, category_name)]
    filtered = sort_recipes(filtered, sort)
    return paginate(filtered, page, limit)
