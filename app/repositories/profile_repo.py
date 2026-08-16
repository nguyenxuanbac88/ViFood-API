from app.models.user_profile import UserProfile
from app.repositories.base_repo import BaseRepository
from app.helpers.convert_time import to_vn_time

from app.schemas.update_profile import UpdateProfileRequest


class UserProfileRepository(BaseRepository):
    
    def __init__(self, db):
        super().__init__(db)

    # =========================
    # BASIC
    # =========================
    
    def _map_profile(self, record) -> UserProfile:
        p = record["p"]

        return UserProfile(
            profile_id=p.get("id"),
            first_name=p.get("firstName"),
            last_name=p.get("lastName"),
            avatar=p.get("avatar"),
            created_at=to_vn_time(p.get("createdAt")),
            updated_at=to_vn_time(p.get("updatedAt")),
        )
        
    def _map_profile_with_relations(self, record):
        p = record["p"]
        return {
            "profile_id": p.get("id"),
            "first_name": p.get("firstName"),
            "last_name": p.get("lastName"),
            "avatar": p.get("avatar"),
        }
        
    def create_profile(self, user_id: str, profile: UserProfile):

        profile_data = self.prepare_entity({
            "firstName": profile.first_name,
            "lastName": profile.last_name,
            "avatar": profile.avatar,
        })
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                CREATE (p:Profile $profile)
                CREATE (u)-[:HAS_FAMILY_MEMBER]->(p)
                RETURN p
            """, {
                "user_id": user_id,
                "profile": profile_data
            }).single()

            if not result:
                return None

            return self._map_profile(result)

        return self.write(query)

    def get_user_profile_by_user_id(self, user_id: str) -> UserProfile | None:

        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:HAS_PROFILE]->(p:Profile)
                RETURN p
                LIMIT 1
            """, {
                "user_id": user_id
            })

            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.read(query)
    
    def get_profile_by_user_access(self, user_id: str, profile_id: str) -> UserProfile:
    
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})
                MATCH (u)-[:HAS_PROFILE|HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                RETURN p
                LIMIT 1
            """, {
                "user_id": user_id,
                "profile_id": profile_id
            })

            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.read(query)
    
    def update_user_profile(self, user_id: str, profile_id: str, profile: UpdateProfileRequest) -> UserProfile | None:
        
        profile_data = self.prepare_update_entity({
            "firstName": profile.first_name,
            "lastName": profile.last_name,
            "avatar": profile.avatar
        })
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_PROFILE|HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                
                SET p += $profile_data
                    
                RETURN p
                LIMIT 1
                """, {
                    "user_id": user_id,
                    "profile_id": profile_id,
                    "profile_data": profile_data,
                })
            record = result.single()

            if not record:
                return None

            return self._map_profile(record)

        return self.write(query)
    
    def delete_family_member(self, user_id: str, profile_id: str) -> bool:
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_FAMILY_MEMBER]->(p:Profile {id: $profile_id})
                DETACH DELETE p
                RETURN count(*) > 0 AS deleted
                """, {
                    "user_id": user_id,
                    "profile_id": profile_id,
                })
            record = result.single()

            return record["deleted"]

        return self.write(query)

    # =========================
    # FAMILY MEMBERS
    # =========================
    
    def get_family_members(self, user_id: str) -> list[UserProfile]:
        
        def query(tx):
            result = tx.run("""
                MATCH (u:User {id: $user_id})-[:HAS_FAMILY_MEMBER]->(p:Profile)
                RETURN p
            """, {
                "user_id": user_id
            })

            return [self._map_profile(r) for r in result]

        return self.read(query)
