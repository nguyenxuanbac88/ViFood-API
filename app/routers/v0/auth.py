from fastapi import APIRouter, HTTPException

from app.schemas.auth import RegisterRequest
from app.services.v0.auth_service import AuthServiceV0

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_service = AuthServiceV0()


@router.post("/register")
def register(data: RegisterRequest):

    user = auth_service.register_user(data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "Register success",
        "data": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "profile_id": user.profile_id
        }
    }
    

@router.get("/users")
def get_all_users():
    users = auth_service.get_all_users()

    return {
        "message": "Get all users success",
        "data": users
    }
    

@router.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    user = auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Get user by id success",
        "data": user
    }
