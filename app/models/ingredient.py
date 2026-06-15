from typing import Optional

from pydantic import BaseModel

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect


class Ingredient(BaseModel):
    id: Optional[str] = None
    name: str
    key: Optional[str] = None
    description: str | None = None
