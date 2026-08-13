from datetime import datetime, timezone
from typing import Any


class ScanHistoryService:
    def __init__(self, settings):
        self.settings = settings

    def save_success(
        self,
        *,
        user_id: str,
        analysis_id: str,
        image_ref: str,
        result: dict[str, Any],
    ) -> None:
        collection = self._get_collection()
        if collection is None:
            return

        collection.insert_one(
            {
                "user_id": user_id,
                "analysis_id": analysis_id,
                "image_ref": image_ref,
                "result": result,
                "status": "success",
                "created_at": datetime.now(timezone.utc),
            }
        )

    def list_for_user(self, *, user_id: str, limit: int = 50) -> list[dict[str, Any]]:
        collection = self._get_collection()
        if collection is None:
            return []

        documents = collection.find(
            {"user_id": user_id},
            sort=[("created_at", -1)],
            limit=limit,
        )
        return [self._to_public_document(document) for document in documents]

    def get_for_user(
        self,
        *,
        user_id: str,
        analysis_id: str,
    ) -> dict[str, Any] | None:
        collection = self._get_collection()
        if collection is None:
            return None

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
            return None

        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("MongoDB driver is not installed") from exc

        client = MongoClient(self.settings.mongodb_uri)
        return client[self.settings.mongodb_database][
            self.settings.mongodb_scan_history_collection
        ]

    def _to_public_document(self, document: dict[str, Any]) -> dict[str, Any]:
        public_document = dict(document)
        public_document.pop("_id", None)
        return public_document
