from app.models.allergy import Allergy
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.repositories.allergy_repo import AllergyRepository
from app.db import db


class AllergyServiceV0:

    def __init__(self):
        self.repo = AllergyRepository(db)

    def get_all_allergies(self):
        return self.repo.get_all()

    def get_allergy_by_id(self, allergy_id: int):
        return self.repo.get_by_id(allergy_id)
    def create_allergy(
        self,
        name: str,
        description: str | None = None,
        code: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        new_id = len(self.repo.get_all()) + 1

        new_allergy = Allergy(
            id=new_id,
            name=name,
            code=code,
            description=description,
            image=image,
            effects=effects or [],
            found_in=found_in or []
        )

        return self.repo.create(new_allergy)

    def update_allergy(
        self,
        allergy_id: int,
        name: str,
        description: str | None = None,
        code: str | None = None,
        image: str | None = None,
        effects: list[HealthEffect] | None = None,
        found_in: list[FoodCategory] | None = None
    ):
        allergy = self.repo.get_by_id(allergy_id)

        if not allergy:
            return None

        allergy.name = name
        allergy.description = description
        allergy.code = code
        allergy.image = image
        allergy.effects = effects or []
        allergy.found_in = found_in or []

        return allergy

    def delete_allergy(self, allergy_id: int):
        return self.repo.delete(allergy_id)