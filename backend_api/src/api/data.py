"""
In-memory seed data and helper functions for the Recipe Explorer API.

No external database is used in this initial implementation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List

PLACEHOLDER_IMAGE = "https://picsum.photos/seed/recipe/600/400"


def _recipe(
    recipe_id: int,
    title: str,
    description: str,
    category: str,
    ingredients: List[Dict[str, str]],
    steps: List[str],
    image_seed: str,
    rating_avg: float,
    rating_count: int,
) -> Dict:
    """Create a consistent recipe dict."""
    return {
        "id": recipe_id,
        "title": title,
        "description": description,
        "category": category,
        "ingredients": ingredients,
        "steps": steps,
        "image": f"https://picsum.photos/seed/{image_seed}/600/400",
        "rating_avg": rating_avg,
        "rating_count": rating_count,
    }


# Seeded recipes (~10)
RECIPES: List[Dict] = [
    _recipe(
        1,
        "Lemon Herb Chicken",
        "Juicy chicken thighs with lemon, garlic, and fresh herbs.",
        "Dinner",
        [
            {"name": "chicken thighs", "quantity": "6"},
            {"name": "lemon", "quantity": "1"},
            {"name": "garlic", "quantity": "3 cloves"},
            {"name": "olive oil", "quantity": "2 tbsp"},
            {"name": "rosemary", "quantity": "1 tsp"},
            {"name": "salt", "quantity": "to taste"},
        ],
        [
            "Preheat oven to 425°F (220°C).",
            "Mix lemon juice, minced garlic, olive oil, rosemary, and salt.",
            "Coat chicken and bake for 30-35 minutes until cooked through.",
        ],
        "lemon-chicken",
        4.6,
        24,
    ),
    _recipe(
        2,
        "Avocado Toast (Café Style)",
        "Creamy avocado toast with lemon and chili flakes.",
        "Breakfast",
        [
            {"name": "bread", "quantity": "2 slices"},
            {"name": "avocado", "quantity": "1"},
            {"name": "lemon", "quantity": "1/2"},
            {"name": "chili flakes", "quantity": "pinch"},
            {"name": "salt", "quantity": "to taste"},
        ],
        [
            "Toast the bread.",
            "Mash avocado with lemon juice, salt, and chili flakes.",
            "Spread on toast and serve immediately.",
        ],
        "avocado-toast",
        4.3,
        15,
    ),
    _recipe(
        3,
        "Classic Tomato Basil Pasta",
        "Simple pasta with rich tomato sauce and basil.",
        "Dinner",
        [
            {"name": "pasta", "quantity": "250g"},
            {"name": "tomatoes", "quantity": "4"},
            {"name": "garlic", "quantity": "2 cloves"},
            {"name": "basil", "quantity": "1 handful"},
            {"name": "olive oil", "quantity": "2 tbsp"},
        ],
        [
            "Cook pasta until al dente.",
            "Sauté garlic in olive oil, add chopped tomatoes and simmer.",
            "Toss pasta with sauce and basil.",
        ],
        "tomato-basil-pasta",
        4.4,
        31,
    ),
    _recipe(
        4,
        "Cucumber Mint Salad",
        "Refreshing salad with cucumber, mint, and yogurt dressing.",
        "Salads",
        [
            {"name": "cucumber", "quantity": "2"},
            {"name": "mint", "quantity": "10 leaves"},
            {"name": "yogurt", "quantity": "1/2 cup"},
            {"name": "lemon", "quantity": "1/2"},
            {"name": "salt", "quantity": "to taste"},
        ],
        [
            "Slice cucumber and chop mint.",
            "Mix yogurt with lemon juice and salt.",
            "Combine and chill before serving.",
        ],
        "cucumber-mint-salad",
        4.1,
        9,
    ),
    _recipe(
        5,
        "Chocolate Chip Cookies",
        "Soft cookies with melty chocolate chips.",
        "Dessert",
        [
            {"name": "flour", "quantity": "2 cups"},
            {"name": "butter", "quantity": "1/2 cup"},
            {"name": "sugar", "quantity": "3/4 cup"},
            {"name": "egg", "quantity": "1"},
            {"name": "chocolate chips", "quantity": "1 cup"},
        ],
        [
            "Preheat oven to 350°F (175°C).",
            "Cream butter and sugar, add egg, then fold in flour and chips.",
            "Bake 10-12 minutes.",
        ],
        "cookies",
        4.8,
        58,
    ),
    _recipe(
        6,
        "Veggie Stir-Fry",
        "Colorful vegetables stir-fried with soy sauce and sesame.",
        "Dinner",
        [
            {"name": "broccoli", "quantity": "2 cups"},
            {"name": "carrot", "quantity": "1"},
            {"name": "bell pepper", "quantity": "1"},
            {"name": "soy sauce", "quantity": "2 tbsp"},
            {"name": "sesame oil", "quantity": "1 tsp"},
        ],
        [
            "Heat pan and add sesame oil.",
            "Stir-fry vegetables until crisp-tender.",
            "Add soy sauce and toss.",
        ],
        "stir-fry",
        4.2,
        18,
    ),
    _recipe(
        7,
        "Greek Yogurt Parfait",
        "Layered yogurt parfait with berries and granola.",
        "Breakfast",
        [
            {"name": "greek yogurt", "quantity": "1 cup"},
            {"name": "berries", "quantity": "1 cup"},
            {"name": "granola", "quantity": "1/2 cup"},
            {"name": "honey", "quantity": "1 tbsp"},
        ],
        [
            "Layer yogurt, berries, and granola in a glass.",
            "Drizzle honey on top.",
        ],
        "parfait",
        4.5,
        22,
    ),
    _recipe(
        8,
        "Creamy Mushroom Soup",
        "Comforting mushroom soup with a velvety finish.",
        "Soups",
        [
            {"name": "mushrooms", "quantity": "300g"},
            {"name": "onion", "quantity": "1"},
            {"name": "garlic", "quantity": "2 cloves"},
            {"name": "cream", "quantity": "1/2 cup"},
            {"name": "vegetable stock", "quantity": "3 cups"},
        ],
        [
            "Sauté onion and garlic, add mushrooms and cook down.",
            "Add stock and simmer 15 minutes.",
            "Blend partially and stir in cream.",
        ],
        "mushroom-soup",
        4.4,
        12,
    ),
    _recipe(
        9,
        "Tuna Salad Wrap",
        "Quick tuna salad wrapped in a tortilla with greens.",
        "Lunch",
        [
            {"name": "tuna", "quantity": "1 can"},
            {"name": "mayonnaise", "quantity": "2 tbsp"},
            {"name": "celery", "quantity": "1 stalk"},
            {"name": "tortilla", "quantity": "1"},
            {"name": "lettuce", "quantity": "1 handful"},
        ],
        [
            "Mix tuna with mayo and chopped celery.",
            "Add lettuce to tortilla, top with tuna salad.",
            "Wrap tightly and slice.",
        ],
        "tuna-wrap",
        4.0,
        7,
    ),
    _recipe(
        10,
        "Berry Smoothie",
        "Bright berry smoothie with banana and yogurt.",
        "Drinks",
        [
            {"name": "berries", "quantity": "1 cup"},
            {"name": "banana", "quantity": "1"},
            {"name": "yogurt", "quantity": "1/2 cup"},
            {"name": "milk", "quantity": "1/2 cup"},
        ],
        [
            "Add all ingredients to blender.",
            "Blend until smooth and serve.",
        ],
        "berry-smoothie",
        4.7,
        33,
    ),
]

# Derived categories
CATEGORIES: List[Dict[str, str]] = sorted(
    [{"name": c} for c in {r["category"] for r in RECIPES}],
    key=lambda x: x["name"].lower(),
)

# Mock user storage
MOCK_USER_ID = "user_1"
FAVORITES_BY_USER: Dict[str, List[int]] = {MOCK_USER_ID: [1, 5]}
RATINGS_BY_USER: Dict[str, Dict[int, int]] = {MOCK_USER_ID: {1: 5, 3: 4, 5: 5}}


# PUBLIC_INTERFACE
def get_seed_recipes() -> List[Dict]:
    """Return a deep copy of seeded recipes (to avoid accidental mutation)."""
    return deepcopy(RECIPES)
