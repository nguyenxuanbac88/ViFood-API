from datetime import date, datetime, timezone

import pytest

from app.services.scan_history_service import ScanHistoryService


class FakeSettings:
    mongodb_uri = "mongodb://localhost:27017"
    mongodb_database = "vifood"
    mongodb_scan_history_collection = "scan_history"
    app_version = "test-version"


class FakeCollection:
    def __init__(self):
        self.documents = []

    def insert_one(self, document):
        self.documents.append(document)

    def find(self, query, sort=None, limit=50):
        records = []
        for document in self.documents:
            if document["user_id"] != query["user_id"]:
                continue

            created_at_filter = query.get("created_at")
            if created_at_filter:
                created_at = document["created_at"]
                if created_at < created_at_filter["$gte"]:
                    continue
                if created_at > created_at_filter["$lte"]:
                    continue

            records.append(document)
        records.sort(key=lambda item: item["created_at"], reverse=True)
        return records[:limit]

    def find_one(self, query):
        for document in self.documents:
            if (
                document["user_id"] == query["user_id"]
                and document["analysis_id"] == query["analysis_id"]
            ):
                return document
        return None


class FakeS3Service:
    def create_download_url(self, s3_key: str) -> str:
        return f"https://cdn.example.test/{s3_key}"


class FakeScanHistoryService(ScanHistoryService):
    def __init__(self):
        super().__init__(FakeSettings(), s3_service=FakeS3Service())
        self.collection = FakeCollection()

    def _get_collection(self):
        return self.collection


def test_save_success_stores_completed_history_document():
    service = FakeScanHistoryService()

    service.save_success(
        user_id="user-1",
        analysis_id="analysis-1",
        image_ref="users/user-1/scans/image.jpg",
        result={"product_name": "Sữa ABC"},
        image_content_type="image/jpeg",
        processing_time_ms=1234,
    )

    assert len(service.collection.documents) == 1
    document = service.collection.documents[0]
    assert document["user_id"] == "user-1"
    assert document["analysis_id"] == "analysis-1"
    assert document["image_ref"] == "users/user-1/scans/image.jpg"
    assert document["image_content_type"] == "image/jpeg"
    assert document["status"] == "completed"
    assert document["result"] == {"product_name": "Sữa ABC"}
    assert document["error"] is None
    assert document["service_version"] == "test-version"
    assert document["processing_time_ms"] == 1234
    assert isinstance(document["created_at"], datetime)
    assert isinstance(document["updated_at"], datetime)


def test_list_for_user_returns_scoped_summary_items():
    service = FakeScanHistoryService()
    service.collection.documents = [
        {
            "user_id": "user-1",
            "analysis_id": "analysis-1",
            "image_ref": "image-1.jpg",
            "status": "completed",
            "result": {
                "product_name": "Sữa ABC",
                "warning": "Có chứa sữa",
            },
            "created_at": datetime(2026, 8, 13, 1, 0, tzinfo=timezone.utc),
        },
        {
            "user_id": "user-2",
            "analysis_id": "analysis-2",
            "image_ref": "image-2.jpg",
            "status": "completed",
            "result": {"product_name": "Bánh XYZ"},
            "created_at": datetime(2026, 8, 13, 2, 0, tzinfo=timezone.utc),
        },
    ]

    result = service.list_for_user(user_id="user-1")

    assert result == [
        {
            "analysis_id": "analysis-1",
            "product_name": "Sữa ABC",
            "image_ref": "image-1.jpg",
            "image_url": "https://cdn.example.test/image-1.jpg",
            "status": "completed",
            "warning": "Có chứa sữa",
            "created_at": "2026-08-13T01:00:00+00:00",
        }
    ]


def test_list_for_user_filters_by_vietnam_calendar_date():
    service = FakeScanHistoryService()
    service.collection.documents = [
        {
            "user_id": "user-1",
            "analysis_id": "analysis-in-date",
            "image_ref": "image-1.jpg",
            "status": "completed",
            "result": {"product_name": "Sữa ABC"},
            "created_at": datetime(2026, 8, 12, 17, 30, tzinfo=timezone.utc),
        },
        {
            "user_id": "user-1",
            "analysis_id": "analysis-out-date",
            "image_ref": "image-2.jpg",
            "status": "completed",
            "result": {"product_name": "Bánh XYZ"},
            "created_at": datetime(2026, 8, 13, 17, 1, tzinfo=timezone.utc),
        },
    ]

    result = service.list_for_user(
        user_id="user-1",
        scanned_date=date(2026, 8, 13),
    )

    assert [item["analysis_id"] for item in result] == ["analysis-in-date"]


def test_get_for_user_returns_only_owned_detail():
    service = FakeScanHistoryService()
    service.collection.documents = [
        {
            "_id": "internal-id",
            "user_id": "user-1",
            "analysis_id": "analysis-1",
            "image_ref": "image-1.jpg",
            "status": "completed",
            "result": {"product_name": "Sữa ABC"},
            "created_at": datetime(2026, 8, 13, 1, 0, tzinfo=timezone.utc),
        }
    ]

    owned = service.get_for_user(user_id="user-1", analysis_id="analysis-1")
    foreign = service.get_for_user(user_id="user-2", analysis_id="analysis-1")

    assert owned == {
        "user_id": "user-1",
        "analysis_id": "analysis-1",
        "image_ref": "image-1.jpg",
        "image_url": "https://cdn.example.test/image-1.jpg",
        "status": "completed",
        "result": {"product_name": "Sữa ABC"},
        "created_at": "2026-08-13T01:00:00+00:00",
    }
    assert foreign is None


def test_missing_mongodb_uri_is_configuration_error():
    class MissingMongoSettings(FakeSettings):
        mongodb_uri = None

    service = ScanHistoryService(MissingMongoSettings())

    with pytest.raises(RuntimeError, match="MongoDB URI is not configured"):
        service.list_for_user(user_id="user-1")
