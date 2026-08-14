from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.services.scan_history_service import ScanHistoryService


router = APIRouter(
    prefix="/scan-history",
    tags=["Scan History V1"],
)

scan_history_service = ScanHistoryService(settings)


@router.get(
    "",
    summary="Lấy lịch sử quét của người dùng hiện tại",
)
async def list_scan_history(
    limit: int = Query(default=50, ge=1, le=100),
    date: date | None = Query(
        default=None,
        description="Ngày cần lấy lịch sử theo định dạng YYYY-MM-DD, tính theo múi giờ Việt Nam.",
    ),
    current_user=Depends(get_current_user),
):
    try:
        records = scan_history_service.list_for_user(
            user_id=current_user["user_id"],
            limit=limit,
            scanned_date=date,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Scan history storage is not available",
        ) from exc

    return {
        "message": "Get scan history success",
        "data": records,
    }


@router.get(
    "/{analysis_id}",
    summary="Lấy chi tiết một lần quét của người dùng hiện tại",
)
async def get_scan_history_detail(
    analysis_id: str,
    current_user=Depends(get_current_user),
):
    try:
        record = scan_history_service.get_for_user(
            user_id=current_user["user_id"],
            analysis_id=analysis_id,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Scan history storage is not available",
        ) from exc

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan history not found",
        )

    return {
        "message": "Get scan history detail success",
        "data": record,
    }
