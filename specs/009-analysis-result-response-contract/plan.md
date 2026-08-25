# Implementation Plan: Contract Response Kết Quả Phân Tích

**Branch**: `009-analysis-result-response-contract` | **Date**: 2026-07-08 | **Spec**: `spec.md`

**Input**: Đặc tả chức năng từ `/specs/009-analysis-result-response-contract/spec.md`

## Summary

Xây dựng và kiểm chứng contract response public của ViFood-API để NutriQuor hiển thị kết quả phân tích nhãn thực phẩm. Feature này bắt đầu sau khi `004-product-extraction` có result hợp lệ và tập trung vào envelope, schema `data`, field public, mapping an toàn và đồng bộ với model/UI iOS.

## Technical Context

**Language/Version**: Python/FastAPI  
**Primary Dependencies**: FastAPI, Pydantic, pytest, service/schema layer hiện có  
**Storage**: Không sở hữu storage; chỉ dùng `image_ref`/`image_url` public sau success path nếu có  
**Testing**: `python -m pytest -q`, contract/schema tests, iOS model contract review  
**Target Platform**: Backend API service  
**Project Type**: web-service  
**Performance Goals**: Mapping response nhẹ, không gọi thêm downstream để render app.  
**Constraints**: Không gọi Builder/AIaaS/S3/MongoDB/Neo4j trực tiếp trong feature response; không expose internal payload.  
**Scale/Scope**: Contract success response cho kết quả phân tích và dữ liệu app result display cần.

## Constitution Check

- Backend API là public boundary duy nhất cho app: PASS.
- Success response dùng envelope `{ message, data }`: REQUIRED.
- Public `data` khớp model iOS `Product`: REQUIRED.
- Không leak internal Builder/S3/MongoDB/Neo4j/debug/provenance: REQUIRED.
- Task phải truy vết được từ spec/plan/tasks đến test và human confirmation: REQUIRED.

## AI4SE Execution Flow

```text
Sys-docs API/data-model + root AGENTS.md + ViFood-API/AGENTS.md
  -> spec.md này
  -> plan.md này
  -> tasks.md
  -> contract sync + API change + iOS integration skills
  -> Codex rà schema/service/router/tests
  -> pytest/contract/manual verification
  -> con người xác nhận
  -> ghi evidence AI4SE
```

## Verification Strategy

- Chạy `python -m pytest -q` hoặc test subset liên quan contract products.
- Kiểm tra success response có `message` và `data`.
- Kiểm tra `data` có field public khớp `NutriQuor/NutriQuor/Models/Product.swift`.
- Kiểm tra `ingredients`/`additives`/`nutritions` và `ingredient_items`/`additive_items`/`nutrient_items` giữ tên field ổn định.
- Kiểm tra `warning`, `image_ref`, `image_url`, `analysis_id` chỉ xuất hiện khi có dữ liệu public hợp lệ.
- Kiểm tra response không có raw Builder response, debug/provenance, raw MongoDB/Neo4j object, stack trace, token, secret hoặc raw image/base64.

## Project Structure

```text
app/routers/v1/product_v1.py
app/services/v1/product_service_v1.py
app/schemas
tests/test_products_contract.py
tests/test_product_service_v1.py
```

**Structure Decision**: Dùng router/service/schema hiện có của `products` để trả envelope public. Không tạo endpoint mới cho result display; app vẫn nhận result qua `POST /products/extract` và history detail khi cần.

## Complexity Tracking

Không có vi phạm constitution được chấp nhận. Nếu contract response đổi, phải cập nhật đồng bộ Sys-docs, NutriQuor model/UI spec và tests.
