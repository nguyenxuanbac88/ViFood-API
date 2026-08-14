
from app.models.user_profile import UserProfile

from app.repositories.profile_repo import UserProfileRepository
from app.repositories.user_repo import UserRepository
from app.schemas.update_profile import UpdateProfileRequest

from app.models.allergy import Allergy


class UserProfileServiceV1:
    
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.profile_repo = UserProfileRepository(db)

    # =========================
    # PROFILE
    # =========================
        
    def get_family_members(
        self,
        current_user_id: str,
    ) -> list[UserProfile]:

        profile = self.profile_repo.get_family_members(
            current_user_id
        )

        return profile

    def create_user_profile(
        self,
        current_user_id: str,
        first_name: str,
        last_name: str,
        avatar: str | None = None
    ) -> UserProfile:

        first_name = first_name.strip()
        last_name = last_name.strip()

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")

        profile = UserProfile(
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        )

        created_profile = self.profile_repo.create_profile(
            user_id=current_user_id,
            profile=profile
        )

        return created_profile
    
    def update_user_profile(self, current_user_id: str, profile_id: str, profile: UpdateProfileRequest) -> UserProfile:
        
        first_name = profile.first_name.strip()
        last_name = profile.last_name.strip()

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")
        
        profile = self.profile_repo.update_user_profile(
            current_user_id,
            profile_id,
            profile
        )
        
        if not profile:
            raise ValueError("Profile not found")
        
        return profile
    
    def delete_family_member(self, current_user_id: str, target_profile_id: str) -> bool:
        
        deleted = self.profile_repo.delete_family_member(
            current_user_id,
            target_profile_id
        )
        if not deleted:
            raise ValueError("Profile not found")

        return True
        
    # # =========================
    # # ALLERGIES
    # # =========================
    
    def get_allergies_by_profile_id(
        self,
        current_user_id: str,
        target_profile_id: str
    ) -> list[Allergy]:

        self._validate_profile_access(current_user_id, target_profile_id)

        return self.profile_repo.get_allergies_by_profile_id(
            target_profile_id
        )

    def add_allergy_to_profile(
        self,
        current_user_id: str,
        target_profile_id: str,
        allergy_id: str
    ) -> bool:

        self._validate_profile_access(current_user_id, target_profile_id)

        success = self.profile_repo.add_allergy_to_profile(
            target_profile_id,
            allergy_id
        )

        if not success:
            raise ValueError("Allergy not found")

        return success

    def remove_allergy_from_profile(
        self,
        current_user_id: str,
        target_profile_id: str,
        allergy_id: str
    ) -> bool:

        self._validate_profile_access(current_user_id, target_profile_id)

        success = self.profile_repo.remove_allergy_from_profile(
            target_profile_id,
            allergy_id
        )

        if not success:
            raise ValueError("Allergy not found")

        return success

    # # =========================
    # # ACCESS CONTROL
    # # =========================

    def _validate_profile_access(self, current_user_id: str, target_profile_id: str) -> None:
        profile = self.profile_repo.get_profile_by_user_access(
            current_user_id,
            target_profile_id
        )

        if profile is None:
            raise PermissionError("Access denied")
