from app.models.health_effect import HealthEffect
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class HealthEffectRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def get_all(self):
        return self.db.health_effects

    def get_by_id(self, health_effect_id: int):
        return next((h for h in self.db.health_effects if h.id == health_effect_id), None)

    def create(self, health_effect: HealthEffect):
        self.db.health_effects.append(health_effect)
        return health_effect

    def delete(self, health_effect_id: int):
        self.db.health_effects[:] = [h for h in self.db.health_effects if h.id != health_effect_id]
        return True
