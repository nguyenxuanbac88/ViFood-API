from app.models.additive import Additive
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect

from app.fake_db import additives

class AdditiveServiceV0:
    
    @staticmethod
    def get_all_additives(): return additives

    @staticmethod
    def get_additive_by_id(additive_id: int):
        return next((a for a in additives if a.id == additive_id), None)
    
    @staticmethod
    def create_additive(name: str, description: str | None = None, code: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        new_id = max(a.id for a in additives) + 1 if additives else 1
        new_additive = Additive(id=new_id, name=name, code=code, description=description, image=image,
                                effects=effects or [], found_in=found_in or [])
        additives.append(new_additive)
        return new_additive
    
    @staticmethod
    def update_additive(additive_id: int, name: str, description: str | None = None, code: str | None = None, image: str | None = None,
                        effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
        additive = AdditiveServiceV0.get_additive_by_id(additive_id)
        if additive:
            additive.name = name
            additive.description = description
            additive.code = code
            additive.image = image
            additive.effects = effects or []
            additive.found_in = found_in or []
            return additive
        return None
    
    @staticmethod
    def delete_additive(additive_id: int):
        global additives
        additives = [a for a in additives if a.id != additive_id]
        return {"message": "Additive deleted successfully"}
