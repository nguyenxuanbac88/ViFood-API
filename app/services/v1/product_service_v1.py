import base64
import httpx
from fastapi import HTTPException, UploadFile
from uuid import uuid4

from app.core.config import settings
from app.models.product import Product
from app.services.scan_history_service import ScanHistoryService
from app.services.s3_service import S3Service


class ProductServiceV1:
    BUILDER_INTERNAL_FIELDS = {
        "debug",
        "metadata",
        "provenance",
        "raw",
        "raw_response",
        "source_nodes",
        "trace",
        "kg_contract_version",
        "release_id",
        "release_ids",
    }

    def __init__(self):
        self.s3_service = S3Service(settings)
        self.scan_history_service = ScanHistoryService(settings)
        self.settings = settings

    def create(self) -> Product:
        return Product(
            product_name="Sữa ABC",
            age_range="1-3 tuổi",
            ingredients=[
                "Sữa bột",
                "Đường",
                "Dầu thực vật"
            ],
            additive=[
                "Chất điều vị (INS 621)"
            ],
            nutrition={
                "energy": "450 kcal",
                "protein": "12 g",
                "fat": "18 g",
                "sugar": "20 g"
            },
            manufacturer="Công ty XYZ",
            mfg_date="2025-12-31",
            expiry_date="2027-12-31",
            net_weight="900g",
            allergen="Sản phẩm có chứa sữa",
            warning="Không sử dụng cho trẻ em dưới 3 tuổi",
            origin="Việt Nam"
        )

    async def extract_from_image(self, user_id: str, image: UploadFile) -> dict:
        builder_api_url = (
            f"{self.settings.kg_builder_api_url.rstrip('/')}/"
            f"{self.settings.kg_builder_analyze_path.lstrip('/')}"
        )
        analysis_id = f"analysis_{uuid4()}"
        file_content = await image.read()
        content_type = image.content_type or "image/jpeg"

        self._validate_image(
            file_content=file_content,
            content_type=content_type,
        )

        builder_result = await self._analyze_with_builder(
            builder_api_url=builder_api_url,
            analysis_id=analysis_id,
            file_content=file_content,
            content_type=content_type,
        )

        try:
            image_ref = self.s3_service.upload_file(
                user_id=user_id,
                file_content=file_content,
                content_type=content_type,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Cannot persist analyzed label image",
            ) from exc

        public_result = self._sanitize_builder_result(builder_result)
        public_result.update(
            {
                "analysis_id": analysis_id,
                "image_ref": image_ref,
            }
        )

        try:
            self.scan_history_service.save_success(
                user_id=user_id,
                analysis_id=analysis_id,
                image_ref=image_ref,
                result=public_result,
            )
        except RuntimeError as exc:
            raise HTTPException(
                status_code=503,
                detail="Scan history storage is not available",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Cannot persist scan history",
            ) from exc

        return {
            "message": "Analyze product label success",
            "data": public_result,
        }

    def _validate_image(
        self,
        *,
        file_content: bytes,
        content_type: str,
    ) -> None:
        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty",
            )

        if len(file_content) > self.settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail="Uploaded image is too large",
            )

        if content_type not in S3Service.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported image content type: {content_type}",
            )

    async def _analyze_with_builder(
        self,
        *,
        builder_api_url: str,
        analysis_id: str,
        file_content: bytes,
        content_type: str,
    ) -> dict:
        image_base64 = base64.b64encode(file_content).decode("ascii")

        try:
            async with httpx.AsyncClient(
                timeout=self.settings.kg_builder_timeout_seconds,
            ) as client:
                response = await client.post(
                    builder_api_url,
                    json={
                        "request_id": analysis_id,
                        "image_base64": image_base64,
                        "content_type": content_type,
                        "metadata": {
                            "source": "vifood-api",
                        },
                    },
                )

            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=502,
                detail="Builder analyze request failed",
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=502,
                detail="Cannot connect to Builder analyze service",
            ) from exc

        builder_response = response.json()
        return self._extract_builder_data(builder_response)

    def _extract_builder_data(self, builder_response: dict) -> dict:
        if not isinstance(builder_response, dict):
            raise HTTPException(
                status_code=502,
                detail="Builder returned invalid response",
            )

        if builder_response.get("success") is False:
            raise HTTPException(
                status_code=502,
                detail="Builder analyze request failed",
            )

        if "data" in builder_response:
            data = builder_response["data"]
            if not isinstance(data, dict):
                raise HTTPException(
                    status_code=502,
                    detail="Builder returned invalid data",
                )
            return data

        return builder_response

    def _sanitize_builder_result(self, result: dict) -> dict:
        return {
            key: value
            for key, value in result.items()
            if key not in self.BUILDER_INTERNAL_FIELDS
        }
