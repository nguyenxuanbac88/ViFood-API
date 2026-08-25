# Feature Specification: Contract Response Kết Quả Phân Tích

**Feature Branch**: `009-analysis-result-response-contract`

**Created**: 2026-07-08

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API trả response public ổn định để NutriQuor hiển thị kết quả phân tích nhãn thực phẩm trên ứng dụng."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models/analysis-result-schema.md`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/06-ai4se`, `Sys-docs/08-testing/integration-tests.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-ios-api-integration`, `vifood-ai4se-evidence-log`.
- **Codex Role**: rà soát/sửa schema, service mapping, router response và tests để response public khớp dữ liệu NutriQuor cần render.
- **Human Confirmation**: người phát triển review response contract, kết quả test và xác nhận app hiển thị result đúng.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trả Envelope Public Cho App (Priority: P1)

Backend trả kết quả phân tích qua envelope public `{ message, data }` để app decode ổn định.

**Why this priority**: NutriQuor decode response bằng `APIResponse<Product>`, nên envelope phải ổn định.

**Independent Test**: Gọi hoặc mock `POST /products/extract` thành công và xác nhận response có `message`, `data`, không trả raw Builder payload ở root.

**Acceptance Scenarios**:

1. **Given** extraction thành công, **When** API trả response, **Then** response có envelope `{ message, data }`.
2. **Given** app decode `data` thành `Product`, **When** optional field thiếu, **Then** contract vẫn giữ cấu trúc ổn định và không yêu cầu app tự tạo dữ liệu giả.

---

### User Story 2 - Cung Cấp Dữ Liệu Result Cho NutriQuor (Priority: P1)

Backend trả các field public mà app cần để hiển thị màn kết quả phân tích.

**Why this priority**: Result UI cần dữ liệu đủ nhóm: sản phẩm, dinh dưỡng, cảnh báo, thành phần/phụ gia và thông tin sản phẩm.

**Independent Test**: Mock Builder success result đầy đủ và xác nhận `data` chứa các field public đúng tên.

**Acceptance Scenarios**:

1. **Given** Builder success result có product info, **When** API map response, **Then** `data` có `product_name`, `manufacturer`, `mfg_date`, `expiry_date`, `net_weight`, `origin` nếu có.
2. **Given** Builder success result có nutrients, **When** API map response, **Then** `data` có `nutritions` hoặc `nutrient_items` để app render section dinh dưỡng.
3. **Given** Builder success result có ingredients/additives linked entity, **When** API map response, **Then** `data` có `ingredients`, `additives`, `ingredient_items`, `additive_items` theo contract public.

---

### User Story 3 - Giữ Response Sạch Và Không Lộ Nội Bộ (Priority: P1)

Backend không trả dữ liệu debug, provenance nội bộ, raw database object hoặc stack trace cho app.

**Why this priority**: App là public client; response phải ổn định và an toàn.

**Independent Test**: Mock Builder result có metadata/debug nội bộ và xác nhận API không đưa các field đó vào response public.

**Acceptance Scenarios**:

1. **Given** Builder trả debug/provenance/internal fields, **When** API map response, **Then** public response không chứa các field đó.
2. **Given** storage/history có `s3_key` nội bộ, **When** API trả result, **Then** app chỉ nhận `image_ref`/`image_url` public nếu contract cho phép.
3. **Given** lỗi mapping/schema, **When** API trả lỗi, **Then** response không chứa stack trace hoặc raw exception.

### Edge Cases

- Field optional thiếu không làm response contract phá vỡ app decode.
- Public field phải dùng tên ổn định theo contract mobile/backend.
- Không trả raw Builder response, raw MongoDB document, raw Neo4j node/relationship, secret, token hoặc stack trace.
- `image_ref`/`image_url` là dữ liệu public do Backend API tạo sau storage success; không phải input cho Builder.
- API không gọi AIaaS trực tiếp để bổ sung field cho result.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI trả success response theo envelope `{ "message": "...", "data": ... }`.
- **FR-002**: `data` PHẢI là result public để NutriQuor decode thành `Product`.
- **FR-003**: `data` PHẢI hỗ trợ các field product info: `analysis_id`, `product_name`, `manufacturer`, `mfg_date`, `expiry_date`, `net_weight`, `origin`, `age_range` khi có dữ liệu.
- **FR-004**: `data` PHẢI hỗ trợ `ingredients` và `ingredient_items` khi Builder/API có dữ liệu tương ứng.
- **FR-005**: `data` PHẢI hỗ trợ `additives` và `additive_items` khi Builder/API có dữ liệu tương ứng.
- **FR-006**: `data` PHẢI hỗ trợ `nutritions` và/hoặc `nutrient_items` khi Builder/API có dữ liệu tương ứng.
- **FR-007**: `data` PHẢI hỗ trợ `warning` chỉ khi Backend/Builder có dữ liệu public hợp lệ.
- **FR-008**: `data` PHẢI hỗ trợ `image_ref`/`image_url` public sau khi storage success nếu có.
- **FR-009**: API KHÔNG ĐƯỢC expose raw Builder debug payload, raw database object, stack trace, internal URL, token, secret hoặc raw image/base64.
- **FR-010**: API PHẢI giữ contract đồng bộ với `NutriQuor/NutriQuor/Models/Product.swift` và `NutriQuor/NutriQuor/Features/ScanNutri/AnalystView.swift`.

### Key Entities

- **PublicAnalysisResponse**: envelope thành công `{ message, data }`.
- **PublicProductAnalysis**: object `data` mà app decode thành `Product`.
- **PublicLinkedEntity**: ingredient/additive/nutrient item có `id` public để app mở detail.
- **PublicImageReference**: `image_ref`/`image_url` public do Backend API tạo sau storage success.
- **InternalAnalysisPayload**: dữ liệu Builder/database nội bộ không được expose.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Success response của extraction có envelope `{ message, data }`.
- **SC-002**: `data` decode được bởi model `Product` hiện tại của NutriQuor.
- **SC-003**: Response có đủ field public để app render result sections khi dữ liệu tồn tại.
- **SC-004**: Response không chứa raw Builder/debug/provenance/internal database fields.
- **SC-005**: Pytest contract/schema pass sau thay đổi.
- **SC-006**: Contract sync check xác nhận API response khớp app result display spec `006-analysis-result-display`.
- **SC-007**: Evidence AI4SE ghi rõ file thay đổi, contract check, test result và human confirmation.

## Assumptions

- Product extraction orchestration được đặc tả tại `004-product-extraction`.
- Storage tạo `image_ref`/`image_url` public sau khi Builder success.
- MongoDB history lưu kết quả theo user nhưng không phải nguồn raw response public.
- Neo4j chỉ cung cấp id/detail data qua Builder/API mapping, không trả raw graph object cho app.
