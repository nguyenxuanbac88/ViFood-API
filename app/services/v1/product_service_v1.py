import httpx
from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.models.product import Product
from app.services.s3_service import S3Service


class ProductServiceV1:
    def __init__(self):
        self.s3_service = S3Service(settings)
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
        file_content = await image.read()
        content_type = image.content_type or "image/jpeg"

        s3_key = self.s3_service.upload_file(
            user_id=user_id,
            file_content=file_content,
            content_type=content_type,
        )

        try:
            async with httpx.AsyncClient(timeout=90) as client:
                response = await client.post(
                    builder_api_url,
                    json={
                        "s3_key": s3_key,
                    },
                )

            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise HTTPException(
                status_code=502,
                detail=(
                    "KG Builder analyze request failed "
                    f"with status {exc.response.status_code}: {detail}"
                ),
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Cannot connect to KG Builder at {builder_api_url}: {exc}",
            ) from exc

        result = response.json()

        return {
            "message": "Analyze product label success",
            "data": {
                **result,
                "s3_key": s3_key,
            },
        }
