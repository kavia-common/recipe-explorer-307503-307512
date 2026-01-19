# Recipe Explorer - Backend (FastAPI)

In-memory FastAPI backend providing recipes, categories, ingredient search, favorites, and ratings.

## Run locally

From `backend_api/`:

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

The preview system manages ports; locally the default is typically http://localhost:8000.

## Notes

- Storage is **in-memory only** (seeded recipes, mock user favorites/ratings).
- CORS is enabled for `http://localhost:3000`.
- API docs: `/docs`
- Health: `/health`
