from fastapi import APIRouter
from app.services.v0.health_goal_service import HealthGoalServiceV0

router = APIRouter(
    prefix="/health-goals",
    tags=["Health Goals V0"])


@router.get("/")
def list_health_goals():
    return HealthGoalServiceV0.get_all_health_goals()


@router.get("/{id}")
def get_health_goal_by_id(id: int):
    health_goal = HealthGoalServiceV0.get_health_goal_by_id(id)
    return health_goal or {"error": "Health Goal not found"}


@router.post("/")
def create_health_goal(name: str):
    new_health_goal = HealthGoalServiceV0.create_health_goal(name)
    return new_health_goal


@router.put("/{id}")
def update_health_goal(id: int, name: str):
    updated_health_goal = HealthGoalServiceV0.update_health_goal(id, name)
    return updated_health_goal or {"error": "Health Goal not found"}


@router.delete("/{id}")
def delete_health_goal(id: int):
    result = HealthGoalServiceV0.delete_health_goal(id)
    return result or {"error": "Health Goal not found"}