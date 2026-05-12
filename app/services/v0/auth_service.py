from datetime import datetime

from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.user_repo import UserRepository
from app.repositories.profile_repo import UserProfileRepository
from app.core.security import hash_password


class AuthServiceV0:
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.profile_repo = UserProfileRepository()
    
    
    def register_user(self, data):

            existing_user = self.user_repo.get_user_by_email(data.email)

            if existing_user:
                raise ValueError("Email already exists")

            profile = UserProfile(
                profile_id=self.profile_repo.count_user_profiles() + 1,
                userId=None,
                first_name=data.first_name,
                last_name=data.last_name,
                avatar=None,
                health_goals=[],
                diseases=[],
                allergies=[],
                family_members=[],
                parent_profile_id=None
            )

            user = User(
                id=self.user_repo.count_users() + 1,
                email=data.email,
                password_hash=hash_password(data.password),
                is_active=True,
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                profile_id=profile.profile_id
            )

            created_profile = self.profile_repo.create_user_profile(profile)

            created_user = self.user_repo.create_user(user)

            created_profile.userId = created_user.id

            return created_user


    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all_users()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_user_by_id(user_id)