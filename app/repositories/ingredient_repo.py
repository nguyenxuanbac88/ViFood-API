from app.repositories.base_repo import BaseRepository
from app.schemas.ingredient_v1_schema import (
    IngredientAliasResponse,
    IngredientCategoryResponse,
    IngredientDetailResponse,
    IngredientNodeResponse,
    IngredientSourceResponse,
    IngredientUsageResponse,
)


class IngredientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def _to_string(self, value) -> str | None:
        return str(value) if value is not None else None

    def _map_ingredient_node(self, node) -> IngredientNodeResponse:
        return IngredientNodeResponse(
            id=node.get("id"),
            name=node.get("name"),
            name_vi=node.get("name_vi"),
            name_en=node.get("name_en"),
            wikidata_id=node.get("wikidata_id"),
            description_vi=node.get("description_vi"),
            description_en=node.get("description_en"),
            wikipedia_vi_url=node.get("wikipedia_vi_url"),
            wikipedia_en_url=node.get("wikipedia_en_url"),
            status=node.get("status"),
            created_at=self._to_string(node.get("created_at")),
            updated_at=self._to_string(node.get("updated_at")),
        )

    def _map_alias(self, node) -> IngredientAliasResponse | None:
        if not node or not node.get("name"):
            return None

        return IngredientAliasResponse(
            id=node.get("id"),
            name=node.get("name"),
            language=node.get("language"),
        )

    def _map_category(self, node) -> IngredientCategoryResponse | None:
        if not node or not node.get("name"):
            return None

        return IngredientCategoryResponse(
            id=node.get("id"),
            name=node.get("name"),
            wikidata_id=node.get("wikidata_id"),
        )

    def _map_usage(self, node) -> IngredientUsageResponse | None:
        if not node or not node.get("name"):
            return None

        return IngredientUsageResponse(
            id=node.get("id"),
            name=node.get("name"),
            wikidata_id=node.get("wikidata_id"),
        )

    def _map_source(self, node) -> IngredientSourceResponse | None:
        if not node or not node.get("id"):
            return None

        return IngredientSourceResponse(
            id=node.get("id"),
            name=node.get("name"),
            source_url=node.get("source_url"),
        )

    def _map_detail(self, record) -> IngredientDetailResponse:
        ingredient = self._map_ingredient_node(record["i"])

        return IngredientDetailResponse(
            **ingredient.model_dump(),
            aliases=[
                alias
                for alias in (self._map_alias(node) for node in record.get("aliases", []))
                if alias
            ],
            categories=[
                category
                for category in (
                    self._map_category(node)
                    for node in record.get("categories", [])
                )
                if category
            ],
            usages=[
                usage
                for usage in (self._map_usage(node) for node in record.get("usages", []))
                if usage
            ],
            sources=[
                source
                for source in (self._map_source(node) for node in record.get("sources", []))
                if source
            ],
        )

    def get_all(self) -> list[IngredientNodeResponse]:
        def _query(tx):
            result = tx.run("""
                MATCH (i:Ingredient)
                RETURN i
                ORDER BY coalesce(i.name_vi, i.name, i.name_en, i.id)
            """)
            return [self._map_ingredient_node(record["i"]) for record in result]

        return self.read(_query)

    def get_by_id(self, ingredient_id: str) -> IngredientDetailResponse | None:
        def _query(tx):
            result = tx.run("""
                MATCH (i:Ingredient {id: $id})
                OPTIONAL MATCH (i)<-[:REFERS_TO]-(alias:Alias)
                WITH i, collect(DISTINCT alias) AS aliases
                OPTIONAL MATCH (i)-[:BELONGS_TO]->(category:Ingredient)
                WITH i, aliases, collect(DISTINCT category) AS categories
                OPTIONAL MATCH (i)-[:HAS_USAGE]->(usage:Usage)
                WITH i, aliases, categories, collect(DISTINCT usage) AS usages
                OPTIONAL MATCH (i)-[:SUPPORTED_BY]->(source:Source)
                RETURN
                    i,
                    aliases,
                    categories,
                    usages,
                    collect(DISTINCT source) AS sources
                LIMIT 1
            """, {"id": ingredient_id})

            record = result.single()
            return self._map_detail(record) if record else None

        return self.read(_query)
