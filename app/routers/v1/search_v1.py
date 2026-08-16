from fastapi import APIRouter, HTTPException, Query, status

from app.core.database import neo4j_db
from app.services.v1.search_service_v1 import SearchServiceV1

router = APIRouter(
    prefix="/search",
    tags=["Search V1"]
)


search_service = SearchServiceV1(neo4j_db)


@router.get(
    "/",
    summary="Lấy danh sách nutrient, ingredient, additive"
)
def get_nodes(
    limit: int = Query(default=50, ge=1, le=100)
):
    nodes = search_service.get_all(limit=limit)
    return {
        "message": "Get search nodes success",
        "data": nodes,
    }
    

@router.get(
    "/daily",
    summary="Lấy ngẫu nhiên một node cho mỗi ngày"
)
def get_daily_feature():
    result = search_service.get_daily_feature()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
        
    return {
        "message": "Get daily search node success",
        "data": result,
    }


@router.get(
    "/{id}",
    summary="Lấy chi tiết nutrient, ingredient, additive theo ID"
)
def get_node_by_id(id: str):
    result = search_service.get_by_id(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
        
    return {
        "message": "Get search node detail success",
        "data": result,
    }
