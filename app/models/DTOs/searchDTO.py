from pydantic import BaseModel

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect


class searchDTO(BaseModel):
    id: str
    name: str
    key: str
    code: str | None = None
    description: str | None = None
    type: str
