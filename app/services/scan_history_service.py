from datetime import date, datetime, time, timezone
from typing import Any
from zoneinfo import ZoneInfo

from app.services.s3_service import S3Service


class ScanHistoryService:
    def __init__(self, settings, s3_service: S3Service | None = None):
        self.settings = settings
        self.s3_service = s3_service
        self._client = None

    def save_success(
        self,
        *,
        user_id: str,
        analysis_id: str,
        image_ref: str,
        result: dict[str, Any],
        image_content_type: str | None = None,
        processing_time_ms: int | None = None,
    ) -> None:
        collection = self._get_collection()
        now = datetime.now(timezone.utc)

        collection.insert_one(
            {
                "user_id": user_id,
                "analysis_id": analysis_id,
                "image_ref": image_ref,
                "image_content_type": image_content_type,
                "result": result,
                "error": None,
                "status": "completed",
                "service_version": self.settings.app_version,
                "processing_time_ms": processing_time_ms,
                "created_at": now,
                "updated_at": now,
            }
        )

    def list_for_user(
        self,
        *,
        user_id: str,
        limit: int = 50,
        scanned_date: date | None = None,
    ) -> list[dict[str, Any]]:
        collection = self._get_collection()
        query = self._build_user_query(
            user_id=user_id,
            scanned_date=scanned_date,
        )

        documents = collection.find(
            query,
            sort=[("created_at", -1)],
            limit=limit,
        )
        return [self._to_public_list_item(document) for document in documents]

    def get_for_user(
        self,
        *,
        user_id: str,
        analysis_id: str,
    ) -> dict[str, Any] | None:
        collection = self._get_collection()

        document = collection.find_one(
            {
                "user_id": user_id,
                "analysis_id": analysis_id,
            }
        )
        if not document:
            return None

        return self._to_public_document(document)

    def _get_collection(self):
        if not self.settings.mongodb_uri:
            raise RuntimeError("MongoDB URI is not configured")

        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("MongoDB driver is not installed") from exc

        if self._client is None:
            self._client = MongoClient(self.settings.mongodb_uri)

        return self._client[self.settings.mongodb_database][
            self.settings.mongodb_scan_history_collection
        ]

    def _to_public_document(self, document: dict[str, Any]) -> dict[str, Any]:
        public_document = dict(document)
        public_document.pop("_id", None)
        public_document["image_url"] = self._build_image_url(
            public_document.get("image_ref")
        )
        return self._serialize_dates(public_document)

    def _to_public_list_item(self, document: dict[str, Any]) -> dict[str, Any]:
        result = document.get("result") or {}
        image_ref = document.get("image_ref")
        list_item = {
            "analysis_id": document.get("analysis_id"),
            "product_name": result.get("product_name"),
            "image_ref": image_ref,
            "image_url": self._build_image_url(image_ref),
            "status": document.get("status"),
            "warning": result.get("warning"),
            "created_at": document.get("created_at"),
        }
        return self._serialize_dates(list_item)

    def _build_image_url(self, image_ref: str | None) -> str | None:
        if not image_ref:
            return None

        try:
            s3_service = self.s3_service or S3Service(self.settings)
            return s3_service.create_download_url(image_ref)
        except Exception:
            return None

    def _build_user_query(
        self,
        *,
        user_id: str,
        scanned_date: date | None,
    ) -> dict[str, Any]:
        query: dict[str, Any] = {"user_id": user_id}

        if scanned_date is None:
            return query

        vietnam_tz = ZoneInfo("Asia/Ho_Chi_Minh")
        start_local = datetime.combine(scanned_date, time.min, tzinfo=vietnam_tz)
        end_local = datetime.combine(scanned_date, time.max, tzinfo=vietnam_tz)
        query["created_at"] = {
            "$gte": start_local.astimezone(timezone.utc),
            "$lte": end_local.astimezone(timezone.utc),
        }

        return query

    def _serialize_dates(self, data: dict[str, Any]) -> dict[str, Any]:
        for key, value in list(data.items()):
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data
