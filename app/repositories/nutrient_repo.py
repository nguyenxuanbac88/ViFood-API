from app.models.nutrient import Nutrient
from app.repositories.base_repo import BaseRepository
from app.helpers.slug import generate_key


class NutrientRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)
        
    def _map_nutrient(self, record) -> Nutrient:
        n = record["n"]

        return Nutrient(
            id=n.get("id"),
            name=n.get("name"),
            key=n.get("key"),
            description=n.get("description")
        )

    def get_all(self):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient)
                RETURN n
            """)
            return [self._map_nutrient(r) for r in result]

        return self.read(_query)

    def get_by_id(self, allergy_id: str):
        def _query(tx):
            result = tx.run("""
                MATCH (n:Nutrient {id: $id})
                RETURN n
                LIMIT 1
            """, {"id": allergy_id})

            record = result.single()
            return self._map_nutrient(record) if record else None

        return self.read(_query)

    def create(self, nutrient: Nutrient):

            key = generate_key(nutrient.name)

            nutrient_data = self.prepare_entity({
                "name": nutrient.name,
                "key": key
            })

            def _query(tx):
                result = tx.run("""
                    OPTIONAL MATCH (exist:Nutrient {key: $key})
                    WITH exist
                    WHERE exist IS NULL

                    CREATE (n:Nutrient $props)
                    RETURN n
                """, {
                    "key": key,
                    "props": nutrient_data
                })

                record = result.single()
                return self._map_nutrient(record) if record else None

            return self.write(_query)

    def delete(self, nutrient_id: int):
        self.db.nutrients[:] = [n for n in self.db.nutrients if n.id != nutrient_id]
        return True
