from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class MoodType(str, Enum):
    lazy="lazy"; gym="gym"; party="party"; comfort="comfort"
    healthy="healthy"; quick="quick"; festive="festive"

class UserType(str, Enum):
    student="student"; gym_user="gym_user"; family="family"
    professional="professional"; vegan="vegan"

class IngredientItem(BaseModel):
    name: str
    expiry_days: Optional[int] = None
    quantity: Optional[str] = None

class RecipeRequest(BaseModel):
    ingredients: List[IngredientItem] = Field(..., min_length=1)
    budget: Optional[float] = None
    mood: Optional[MoodType] = None
    user_type: Optional[UserType] = None
    jugaad_mode: bool = False
    reality_roast: bool = False
    servings: int = Field(default=2, ge=1, le=20)
    dietary_restrictions: Optional[List[str]] = None
    cuisine_preference: Optional[str] = None

class MealPlanRequest(BaseModel):
    ingredients: List[IngredientItem]
    days: int = Field(default=7, ge=1, le=14)
    user_type: Optional[UserType] = None
    budget_per_day: Optional[float] = None

class HealthAnalysisRequest(BaseModel):
    recipe_name: str
    ingredients: List[str]
    servings: int = 2
