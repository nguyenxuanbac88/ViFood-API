
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


# =========================
# USER
# =========================

fake_users_db: list[User] = []
