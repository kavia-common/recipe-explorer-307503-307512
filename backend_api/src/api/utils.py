"""
Utility functions for filtering, sorting, and pagination.
"""

from __future__ import annotations

from math import ceil
from typing import Any, Dict, List


# PUBLIC_INTERFACE
def paginate(items: List[Any], page: int, limit: int) -> Dict[str, Any]:
    """Paginate a list and return a dict compatible with PaginatedResponse."""
    page = max(1, page)
    limit = max(1, limit)
    total = len(items)
    total_pages = ceil(total / limit) if total else 0

    start = (page - 1) * limit
    end = start + limit
    sliced = items[start:end]
    return {
        "items": sliced,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }


def _norm(s: str) -> str:
    return s.strip().lower()


# PUBLIC_INTERFACE
def recipe_matches_query(recipe: Dict, q: str) -> bool:
    """Return True if recipe title/description matches query string."""
    nq = _norm(q)
    if not nq:
        return True
    return nq in _norm(recipe.get("title", "")) or nq in _norm(recipe.get("description", ""))


# PUBLIC_INTERFACE
def recipe_matches_category(recipe: Dict, category: str) -> bool:
    """Return True if recipe category matches (case-insensitive)."""
    if not category:
        return True
    return _norm(recipe.get("category", "")) == _norm(category)


# PUBLIC_INTERFACE
def recipe_matches_ingredients_or(recipe: Dict, ingredients_csv: str) -> bool:
    """OR-match: any ingredient name contains any of the provided tokens."""
    if not ingredients_csv:
        return True
    tokens = [_norm(t) for t in ingredients_csv.split(",") if _norm(t)]
    if not tokens:
        return True

    ing_names = [_norm(i.get("name", "")) for i in recipe.get("ingredients", [])]
    for t in tokens:
        if any(t in name for name in ing_names):
            return True
    return False


# PUBLIC_INTERFACE
def recipe_matches_include_all(recipe: Dict, include_csv: str) -> bool:
    """ALL-match: recipe must include all tokens (substring match) in ingredient names."""
    if not include_csv:
        return True
    tokens = [_norm(t) for t in include_csv.split(",") if _norm(t)]
    if not tokens:
        return True

    ing_names = [_norm(i.get("name", "")) for i in recipe.get("ingredients", [])]
    return all(any(t in name for name in ing_names) for t in tokens)


# PUBLIC_INTERFACE
def sort_recipes(recipes: List[Dict], sort_by: str) -> List[Dict]:
    """
    Sort recipes. Supported:
      - 'rating' (desc by rating_avg, then rating_count)
      - 'title' (asc by title)
    """
    key = (sort_by or "").strip().lower()
    if key == "title":
        return sorted(recipes, key=lambda r: _norm(r.get("title", "")))
    if key == "rating":
        return sorted(
            recipes,
            key=lambda r: (float(r.get("rating_avg", 0.0)), int(r.get("rating_count", 0))),
            reverse=True,
        )
    return recipes
