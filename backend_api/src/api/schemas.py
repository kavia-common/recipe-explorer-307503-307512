"""
Pydantic models for the Recipe Explorer API.
"""

from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """Ingredient entry with a name and quantity."""

    name: str = Field(..., description="Ingredient name (lower/upper allowed)")
    quantity: str = Field(..., description="Quantity (free-form)")


class Recipe(BaseModel):
    """Recipe representation."""

    id: int = Field(..., description="Recipe id")
    title: str = Field(..., description="Recipe title")
    description: str = Field(..., description="Short description")
    category: str = Field(..., description="Recipe category")
    image: str = Field(..., description="Image URL")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="Step-by-step instructions")
    rating_avg: float = Field(..., description="Average rating (1-5)")
    rating_count: int = Field(..., description="Number of ratings")


class Category(BaseModel):
    """Category representation."""

    name: str = Field(..., description="Category name")


class Favorite(BaseModel):
    """Favorite record for a mock user."""

    user_id: str = Field(..., description="Mock user id")
    recipe_id: int = Field(..., description="Recipe id")


class Rating(BaseModel):
    """Rating record for a mock user."""

    user_id: str = Field(..., description="Mock user id")
    recipe_id: int = Field(..., description="Recipe id")
    rating: int = Field(..., ge=1, le=5, description="Rating value (1-5)")


class RatingUpsertRequest(BaseModel):
    """Request to set/update a rating."""

    rating: int = Field(..., ge=1, le=5, description="Rating value (1-5)")


class FavoriteCreateRequest(BaseModel):
    """Request to create a favorite."""

    recipe_id: int = Field(..., description="Recipe id to favorite")


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""

    items: List[T] = Field(..., description="Items for current page")
    page: int = Field(..., ge=1, description="Current page (1-indexed)")
    limit: int = Field(..., ge=1, description="Items per page")
    total: int = Field(..., ge=0, description="Total available items")
    total_pages: int = Field(..., ge=0, description="Total pages available")


class RecipeCreatePlaceholderRequest(BaseModel):
    """Placeholder create request; not persisted in this in-memory version."""

    title: str = Field(..., description="Recipe title")
    description: str = Field(..., description="Recipe description")
    category: str = Field(..., description="Category")
    ingredients: List[Ingredient] = Field(..., description="Ingredients")
    steps: List[str] = Field(..., description="Steps")
    image: Optional[str] = Field(None, description="Image URL (optional)")
