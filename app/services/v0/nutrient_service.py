from app.models.nutrient import Nutrient

from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.fake_db import nutrients


class NutrientServiceV0:

    @staticmethod
    def get_all_nutrients(): return nutrients

    @staticmethod
    def get_nutrient_by_id(nutrient_id: int):
        return next((n for n in nutrients if n.id == nutrient_id), None)
    
    @staticmethod
    def create_nutrient(name: str, description: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        new_id = max(n.id for n in nutrients) + 1 if nutrients else 1
        new_nutrient = Nutrient(id=new_id, name=name, description=description, image=image, effects=effects, found_in=found_in)
        nutrients.append(new_nutrient)
        return new_nutrient
    
    @staticmethod
    def update_nutrient(nutrient_id: int, name: str, description: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        nutrient = NutrientServiceV0.get_nutrient_by_id(nutrient_id)
        if nutrient:
            nutrient.name = name
            nutrient.description = description
            nutrient.image = image
            nutrient.effects = effects
            nutrient.found_in = found_in
            return nutrient
        return None
    
    @staticmethod
    def delete_nutrient(nutrient_id: int):
        global nutrients
        nutrients = [n for n in nutrients if n.id != nutrient_id]
        return {"message": "Nutrient deleted successfully"}
