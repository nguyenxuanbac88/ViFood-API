from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.base_repo import BaseRepository
from app.helpers.convert_time import to_iso


class UserRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)

    def get_user_by_email(self, email: str) -> User | None:
        query = """
        MATCH (u:User)
        WHERE u.email = $email
        RETURN u
        LIMIT 1
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, email=email)
            record = result.single()

            if not record:
                return None

            node = record["u"]

            return User(
                id=node.get("id"),
                email=node.get("email"),
                password_hash=node.get("passwordHash")
            )

    def get_all_users(self):

        query = """
        MATCH (u:User)
        RETURN u
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query)

            return [
                dict(record["u"])
                for record in result
            ]

    def get_user_by_id(self, user_id: str):

            query = """
            MATCH (u:User)
            WHERE u.id = $id
            RETURN u
            LIMIT 1
            """

            with self.driver.session(database=self.database) as session:
                result = session.run(
                    query,
                    id=user_id
                )

                record = result.single()

                return dict(record["u"]) if record else None

    def create_user(self, user: User, user_profile: UserProfile):
        user_data = self.prepare_entity({
            "email": user.email,
            "passwordHash": user.password_hash,
            "isActive": user.is_active,
        })

        profile_data = self.prepare_entity({
            "firstName": user_profile.first_name,
            "lastName": user_profile.last_name,
            "avatar": user_profile.avatar,
        })
        
        query = """
        CREATE (u:User)
        SET u = $user

        CREATE (p:Profile)
        SET p = $profile

        CREATE (u)-[:HAS_PROFILE]->(p)

        RETURN u, p
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                user=user_data,
                profile=profile_data
            )

            record = result.single()
            if not record:
                return None

            u = record["u"]

            return User(
                id=u["id"],
                email=u["email"],
                password_hash=u.get("passwordHash"),
                is_active=u.get("isActive"),
                created_at=u.get("createdAt"),
                updated_at=u.get("updatedAt"),
            )

    def count_users(self):

        query = """
        MATCH (u:User)
        RETURN count(u) AS total
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query)

            return result.single()["total"]
        
    def get_current_user(self, user_id: str):
        query = """
        MATCH (u:User {id: $user_id})
        OPTIONAL MATCH (u)-[:HAS_PROFILE]->(p:Profile)
        RETURN u, p
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query, user_id=user_id)
            record = result.single()

            if not record:
                return None

            u = record["u"]
            p = record["p"]

            user_data = {
                "user_id": u.get("id"),
                "email": u.get("email"),
                "is_active": u.get("is_active") if u.get("is_active") is not None else u.get("isActive"),
                "created_at": u.get("created_at") or u.get("createdAt"),
                "updated_at": u.get("updated_at") or u.get("updatedAt"),
            }

            profile_data = None

            if p:
                profile_data = {
                    "profile_id": p.get("id"),
                    "first_name": p.get("first_name") or p.get("firstName"),
                    "last_name": p.get("last_name") or p.get("lastName"),
                    "avatar": p.get("avatar"),
                }

            return {
                "user": user_data,
                "profile": profile_data
            }
