# Tasks: Contract Response Kết Quả Phân Tích

**Input**: Tài liệu thiết kế từ `/specs/009-analysis-result-response-contract/`

**Prerequisites**: `spec.md`, `plan.md`, root `AGENTS.md`, `ViFood-API/AGENTS.md`, Sys-docs API/data-model và spec iOS `NutriQuor/specs/006-analysis-result-display`.

## Phase 1: AI4SE Context Preparation

**Goal**: Đưa contract response vào đúng ngữ cảnh trước khi Codex sửa hoặc review code.

- [ ] T001 Đọc `Sys-docs/03-api-contracts/mobile-backend-api.md` và `Sys-docs/04-data-models/analysis-result-schema.md`.
- [ ] T002 Đọc `ViFood-API/AGENTS.md` và xác nhận API là public boundary duy nhất cho app.
- [ ] T003 Đọc `NutriQuor/specs/006-analysis-result-display` và `NutriQuor/NutriQuor/Models/Product.swift`.
- [ ] T004 Chọn skills: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-ios-api-integration`, `vifood-ai4se-evidence-log`.

## Phase 2: Foundation Review

**Goal**: Xác định router/service/schema/test sở hữu response public.

- [ ] T005 Rà soát `app/routers/v1/product_v1.py`.
- [ ] T006 Rà soát `app/services/v1/product_service_v1.py`.
- [ ] T007 Rà soát schema/model response trong `app/schemas`.
- [ ] T008 Rà soát tests contract hiện có như `tests/test_products_contract.py`.

## Phase 3: User Story 1 - Trả Envelope Public Cho App (P1)

**Goal**: Success response giữ envelope `{ message, data }`.

**Independent Test**: Mock success extraction và assert response root có `message`, `data`.

- [ ] T009 [US1] Kiểm tra router trả success response theo envelope public.
- [ ] T010 [US1] Kiểm tra lỗi không trả stack trace/raw exception.
- [ ] T011 [US1] Kiểm tra app có thể decode `data` thành `Product`.

## Phase 4: User Story 2 - Cung Cấp Dữ Liệu Result Cho NutriQuor (P1)

**Goal**: `data` có đủ field public cho màn result khi dữ liệu tồn tại.

**Independent Test**: Mock Builder/API result đầy đủ và assert field public đúng tên.

- [ ] T012 [US2] Kiểm tra product info: `analysis_id`, `product_name`, `manufacturer`, `mfg_date`, `expiry_date`, `net_weight`, `origin`, `age_range`.
- [ ] T013 [US2] Kiểm tra ingredients/additives: `ingredients`, `additives`, `ingredient_items`, `additive_items`.
- [ ] T014 [US2] Kiểm tra nutritions: `nutritions` và/hoặc `nutrient_items`.
- [ ] T015 [US2] Kiểm tra `warning`, `image_ref`, `image_url` chỉ là field public hợp lệ.

## Phase 5: User Story 3 - Giữ Response Sạch Và Không Lộ Nội Bộ (P1)

**Goal**: Response không chứa dữ liệu nội bộ hoặc nhạy cảm.

**Independent Test**: Mock internal/debug fields và assert public response loại bỏ chúng.

- [ ] T016 [US3] Kiểm tra không expose raw Builder response, debug/provenance hoặc internal URL.
- [ ] T017 [US3] Kiểm tra không expose raw MongoDB/Neo4j object, token, secret, raw image/base64.
- [ ] T018 [US3] Kiểm tra `s3_key` nội bộ không được dùng như dữ liệu app hiển thị nếu contract public không cho phép.
- [ ] T019 [US3] Kiểm tra field optional thiếu không phá app decode.

## Phase 6: Verification And Human Confirmation

**Goal**: Kiểm chứng output AI bằng test/build/checklist và chờ người phát triển xác nhận.

- [ ] T020 Chạy `python -m pytest -q` hoặc test subset phù hợp với product contract.
- [ ] T021 Nếu test không chạy được do môi trường, ghi blocker và dùng checklist review/contract thay thế tạm thời.
- [ ] T022 Đối chiếu với `NutriQuor/specs/006-analysis-result-display` và model `Product`.
- [ ] T023 Người phát triển review response cuối và xác nhận chấp nhận hoặc yêu cầu chỉnh tiếp.
- [ ] T024 Ghi evidence AI4SE: task id, prompt summary, file thay đổi, test/check result, lỗi phát hiện, vòng chỉnh sửa, mức sử dụng output AI và human confirmation.
