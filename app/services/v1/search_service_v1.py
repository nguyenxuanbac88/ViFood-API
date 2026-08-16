from datetime import date, datetime
import random
from zoneinfo import ZoneInfo

from app.services.v1.additive_service_v1 import AdditiveServiceV1
from app.services.v1.ingredient_service_v1 import IngredientServiceV1
from app.services.v1.nutrient_service_v1 import NutrientServiceV1


class SearchServiceV1:
    DAILY_TIMEZONE = ZoneInfo("Asia/Ho_Chi_Minh")

    def __init__(self, db):
        self.nutrient_service = NutrientServiceV1(db)
        self.ingredient_service = IngredientServiceV1(db)
        self.additive_service = AdditiveServiceV1(db)

    def _get_nodes_by_type(self, getter) -> list:
        try:
            return getter()
        except ValueError:
            return []

    def _get_all_nodes(self) -> list:
        results: list = []

        results.extend(self._get_nodes_by_type(
            self.nutrient_service.get_all_nutrients,
        ))
        results.extend(self._get_nodes_by_type(
            self.ingredient_service.get_all_ingredients,
        ))
        results.extend(self._get_nodes_by_type(
            self.additive_service.get_all_additives,
        ))

        return results

    def get_all(self, limit: int = 50, target_date: date | None = None) -> list:
        results = self._get_stable_daily_items(target_date)
        return results[:limit]

    def get_by_id(self, id: str):
        node_type = self._get_node_type(id)

        try:
            if node_type == "nutrient":
                return self.nutrient_service.get_nutrient_by_id(id)

            if node_type == "ingredient":
                return self.ingredient_service.get_ingredient_by_id(id)

            if node_type == "additive":
                return self.additive_service.get_additive_by_id(id)
        except ValueError:
            return None

        return None

    def _get_node_type(self, id: str) -> str | None:
        if id.startswith("NUTRIENT:"):
            return "nutrient"

        if id.startswith("INGREDIENT:"):
            return "ingredient"

        if id.startswith("ADDITIVE:"):
            return "additive"

        return None

    def _get_daily_sort_key(self, item) -> tuple[str, str, str, str]:
        return (
            str(getattr(item, "id", "") or ""),
            str(getattr(item, "name", "") or ""),
            str(getattr(item, "name_vi", "") or ""),
            str(getattr(item, "key", "") or ""),
        )

    def _get_current_daily_date(self, target_date: date | None = None) -> date:
        return target_date or datetime.now(self.DAILY_TIMEZONE).date()

    def _get_stable_daily_items(self, target_date: date | None = None) -> list:
        items = sorted(
            self._get_all_nodes(),
            key=self._get_daily_sort_key,
        )

        current_date = self._get_current_daily_date(target_date)
        rng = random.Random(f"vifood-search:{current_date.isoformat()}")
        rng.shuffle(items)
        return items

    def get_daily_feature(self, target_date: date | None = None):
        items = sorted(
            self._get_all_nodes(),
            key=self._get_daily_sort_key,
        )

        if not items:
            return None

        current_date = self._get_current_daily_date(target_date)
        index = current_date.toordinal() % len(items)
        selected = items[index]
        return self.get_by_id(selected.id) or selected
