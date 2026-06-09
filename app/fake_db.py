
from app.models.additive import Additive
from app.models.allergy import Allergy
from app.models.disease import Disease
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.models.health_goal import HealthGoal
from app.models.ingredient import Ingredient
from app.models.nutrient import Nutrient
from app.models.product import Product, ProductNutrition
from app.models.user import User
from app.models.user_profile import UserProfile

# =========================
# USER PROFILES
# =========================

fake_user_profiles_db: list[UserProfile] = [
    UserProfile(
        profile_id=1,
        user_id=1,
        first_name="Thành",
        last_name="Lâm",
        avatar="https://example.com/avatar.jpg",
        health_goals=[
            HealthGoal(id=1, name="Giảm cân"),
        ],
        diseases=[
            Disease(id=1, name="Tiểu đường"),
        ],
        allergies=[
            Allergy(id=1, name="Gluten"),
        ],
        family_members=[],
        parent_profile_id=None
    ),
]

# =========================
# USER
# =========================

fake_users_db: list[User] = []
