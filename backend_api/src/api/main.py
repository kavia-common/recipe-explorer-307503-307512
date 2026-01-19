"""
FastAPI entrypoint for the Recipe Explorer backend.

Exposes REST APIs for:
- /recipes: browse, search, filter
- /categories: list categories and recipes by category
- /ingredients/search: ingredient-based search
- /favorites: favorites CRUD for a mock user id
- /ratings: ratings CRUD for a mock user id

No external database is used (in-memory only).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import categories, favorites, ingredients, ratings, recipes

openapi_tags = [
    {"name": "health", "description": "Service health and diagnostics"},
    {"name": "recipes", "description": "Recipe browsing, search, filtering, and detail"},
    {"name": "categories", "description": "Recipe categories"},
    {"name": "ingredients", "description": "Ingredient-based search"},
    {"name": "favorites", "description": "Favorites management for a mock user"},
    {"name": "ratings", "description": "Ratings management for a mock user"},
]

app = FastAPI(
    title="Recipe Explorer API",
    description="A lightweight Recipe Explorer backend with in-memory storage.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS: allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns service health status.",
    operation_id="health_check",
)
def health_check():
    """Health endpoint used by preview and local development."""
    return {"status": "ok"}


# Keep "/" for backward compatibility with template
# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["health"],
    summary="Root health check",
    description="Alias for /health.",
    operation_id="root_health_check",
)
def root_health_check():
    """Root endpoint used by earlier scaffold."""
    return {"status": "ok"}


app.include_router(recipes.router)
app.include_router(categories.router)
app.include_router(ingredients.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
