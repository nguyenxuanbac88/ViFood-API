import asyncio
from fastapi import HTTPException

from app.services.v1.product_service_v1 import ProductServiceV1


events = []


class FakeUploadFile:
    content_type = "image/png"

    async def read(self):
        return b"image-bytes"


class FakeS3Service:
    def upload_file(self, user_id: str, file_content: bytes, content_type: str) -> str:
        events.append("s3_upload")
        assert user_id == "user-1"
        assert file_content == b"image-bytes"
        assert content_type == "image/png"
        return "scans/user-1/image.png"

    def create_download_url(self, s3_key: str) -> str:
        assert s3_key == "scans/user-1/image.png"
        return "https://storage.example/scans/user-1/image.png"


class FakeScanHistoryService:
    last_saved = None

    def save_success(self, **kwargs):
        events.append("history_save")
        FakeScanHistoryService.last_saved = kwargs


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "success": True,
            "data": {
                "product_name": "Sua ABC",
                "ingredients": [
                    {
                        "id": "ingredient:sua",
                        "name": "Sua",
                    }
                ],
                "debug": {
                    "internal": True,
                },
            },
        }


class FakeAsyncClient:
    last_post = None

    def __init__(self, timeout: int):
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def post(self, url: str, json: dict):
        events.append("builder_call")
        FakeAsyncClient.last_post = {
            "url": url,
            "json": json,
        }
        return FakeResponse()


class FakeFailingResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "success": False,
            "error": "model unavailable",
        }


class FakeFailingAsyncClient(FakeAsyncClient):
    async def post(self, url: str, json: dict):
        events.append("builder_call")
        FakeAsyncClient.last_post = {
            "url": url,
            "json": json,
        }
        return FakeFailingResponse()


def make_service():
    service = ProductServiceV1()
    service.s3_service = FakeS3Service()
    service.scan_history_service = FakeScanHistoryService()
    service.settings.kg_builder_api_url = "http://builder:8000/"
    service.settings.kg_builder_analyze_path = "/labels/analyze"
    service.settings.kg_builder_timeout_seconds = 90
    service.settings.max_file_size = 1024
    return service


def test_extract_from_image_calls_builder_with_image_payload_before_s3(monkeypatch):
    events.clear()
    FakeAsyncClient.last_post = None
    FakeScanHistoryService.last_saved = None
    service = make_service()

    monkeypatch.setattr(
        "app.services.v1.product_service_v1.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = asyncio.run(
        service.extract_from_image(
            user_id="user-1",
            image=FakeUploadFile(),
        )
    )

    assert FakeAsyncClient.last_post == {
        "url": "http://builder:8000/labels/analyze",
        "json": {
            "request_id": result["data"]["analysis_id"],
            "image_base64": "aW1hZ2UtYnl0ZXM=",
            "content_type": "image/png",
            "metadata": {
                "source": "vifood-api",
            },
        },
    }
    assert "s3_key" not in FakeAsyncClient.last_post["json"]
    assert events == ["builder_call", "s3_upload", "history_save"]
    assert result == {
        "message": "Analyze product label success",
        "data": {
            "analysis_id": result["data"]["analysis_id"],
            "product_name": "Sua ABC",
            "ingredients": [
                {
                    "id": "ingredient:sua",
                    "name": "Sua",
                }
            ],
            "image_ref": "scans/user-1/image.png",
            "image_url": "https://storage.example/scans/user-1/image.png",
        },
    }
    assert FakeScanHistoryService.last_saved["user_id"] == "user-1"
    assert FakeScanHistoryService.last_saved["analysis_id"] == result["data"]["analysis_id"]
    assert FakeScanHistoryService.last_saved["image_ref"] == "scans/user-1/image.png"
    assert FakeScanHistoryService.last_saved["result"] == result["data"]
    assert FakeScanHistoryService.last_saved["image_content_type"] == "image/png"
    assert isinstance(FakeScanHistoryService.last_saved["processing_time_ms"], int)
    assert FakeScanHistoryService.last_saved["processing_time_ms"] >= 0


def test_extract_from_image_does_not_upload_when_builder_fails(monkeypatch):
    events.clear()
    FakeAsyncClient.last_post = None
    service = make_service()

    monkeypatch.setattr(
        "app.services.v1.product_service_v1.httpx.AsyncClient",
        FakeFailingAsyncClient,
    )

    try:
        asyncio.run(
            service.extract_from_image(
                user_id="user-1",
                image=FakeUploadFile(),
            )
        )
    except HTTPException as exc:
        assert exc.status_code == 502
        assert exc.detail == "Builder analyze request failed"
    else:
        raise AssertionError("Expected HTTPException")

    assert events == ["builder_call"]


def test_extract_from_image_rejects_invalid_content_type(monkeypatch):
    class InvalidUploadFile(FakeUploadFile):
        content_type = "application/pdf"

    events.clear()
    FakeAsyncClient.last_post = None
    service = make_service()

    monkeypatch.setattr(
        "app.services.v1.product_service_v1.httpx.AsyncClient",
        FakeAsyncClient,
    )

    try:
        asyncio.run(
            service.extract_from_image(
                user_id="user-1",
                image=InvalidUploadFile(),
            )
        )
    except HTTPException as exc:
        assert exc.status_code == 415
    else:
        raise AssertionError("Expected HTTPException")

    assert events == []
    assert FakeAsyncClient.last_post is None
