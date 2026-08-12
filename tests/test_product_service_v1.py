import asyncio

from app.services.v1.product_service_v1 import ProductServiceV1


class FakeUploadFile:
    content_type = "image/png"

    async def read(self):
        return b"image-bytes"


class FakeS3Service:
    def upload_file(self, user_id: str, file_content: bytes, content_type: str) -> str:
        assert user_id == "user-1"
        assert file_content == b"image-bytes"
        assert content_type == "image/png"
        return "scans/user-1/image.png"


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "product_name": "Sua ABC",
            "ingredients": [
                {
                    "id": "ingredient:sua",
                    "name": "Sua",
                }
            ],
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
        FakeAsyncClient.last_post = {
            "url": url,
            "json": json,
        }
        return FakeResponse()


def test_extract_from_image_calls_kg_builder(monkeypatch):
    service = ProductServiceV1()
    service.s3_service = FakeS3Service()
    service.settings.kg_builder_api_url = "http://builder:8000/"
    service.settings.kg_builder_analyze_path = "/labels/analyze"

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
            "s3_key": "scans/user-1/image.png",
        },
    }
    assert result == {
        "message": "Analyze product label success",
        "data": {
            "product_name": "Sua ABC",
            "ingredients": [
                {
                    "id": "ingredient:sua",
                    "name": "Sua",
                }
            ],
            "s3_key": "scans/user-1/image.png",
        },
    }
