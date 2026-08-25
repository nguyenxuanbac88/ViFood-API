# Feature Specification: Phân Tích Ảnh Nhãn

**Feature Branch**: `004-product-extraction`

**Created**: 2026-07-04

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API nhận ảnh nhãn từ app, validate, gửi payload ảnh cho Builder trước khi lưu S3/MongoDB, xử lý lỗi downstream an toàn và bàn giao kết quả hợp lệ cho contract response public."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/03-api-contracts/backend-builder-api.md`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/08-testing/integration-tests.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-debug-extraction-flow`, `vifood-check-aiaas-contract`, `vifood-contract-sync-check`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gửi Ảnh Nhãn Để Phân Tích (Priority: P1)

Người dùng gửi ảnh nhãn thực phẩm từ app để Backend điều phối phân tích qua Builder.

**Why this priority**: Đây là luồng nghiệp vụ trung tâm của toàn bộ hệ thống.

**Independent Test**: Upload multipart image hợp lệ và mock Builder trả kết quả hợp lệ.

**Acceptance Scenarios**:

1. **Given** user đã đăng nhập và ảnh hợp lệ, **When** app gọi `POST /products/extract`, **Then** Backend gửi payload ảnh đến Builder trước khi lưu ảnh.
2. **Given** ảnh không hợp lệ, **When** app gọi endpoint, **Then** Backend trả lỗi validation trước khi gọi Builder.

---

### User Story 2 - Xử Lý Lỗi Builder An Toàn (Priority: P1)

Backend xử lý lỗi Builder mà không ghi nhận scan thành công.

**Why this priority**: Tránh lưu ảnh/history sai khi phân tích thất bại.

**Independent Test**: Mock Builder timeout/lỗi và xác nhận không gọi success storage/history path.

**Acceptance Scenarios**:

1. **Given** Builder trả lỗi, **When** app gửi ảnh, **Then** Backend trả lỗi public có kiểm soát.
2. **Given** Builder timeout, **When** app gửi ảnh, **Then** Backend không lưu ảnh/history thành công.

---

### User Story 3 - Bàn Giao Kết Quả Hợp Lệ Cho Response Contract (Priority: P2)

Backend xác nhận kết quả Builder hợp lệ và bàn giao sang feature response contract public để trả cho app.

**Why this priority**: Flow extraction cần ranh giới rõ giữa điều phối phân tích và contract public mà app sử dụng.

**Independent Test**: Mock Builder response đủ field và xác nhận extraction service chuyển dữ liệu hợp lệ sang success path, còn format response public thuộc `009-analysis-result-response-contract`.

**Acceptance Scenarios**:

1. **Given** Builder trả result hợp lệ, **When** Backend nhận response, **Then** Backend xác nhận result hợp lệ và chuyển sang success path.
2. **Given** Builder trả thiếu field bắt buộc, **When** Backend validate, **Then** Backend trả lỗi processing public.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public chi tiết thuộc `009-analysis-result-response-contract` và không được chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI expose `POST /products/extract` nhận multipart image từ app.
- **FR-002**: API PHẢI yêu cầu current user đã xác thực cho extraction.
- **FR-003**: API PHẢI validate content type/size trước khi gọi Builder.
- **FR-004**: API PHẢI gọi Builder bằng ảnh/payload ảnh, `content_type`, `request_id` và trace metadata trước khi lưu S3.
- **FR-005**: API KHÔNG ĐƯỢC gửi `s3_key` hoặc `image_ref` làm input phân tích cho Builder.
- **FR-006**: API KHÔNG ĐƯỢC gọi trực tiếp AIaaS trong flow chính.
- **FR-007**: API PHẢI coi Builder invalid response/timeout/failure là phân tích thất bại.
- **FR-008**: API PHẢI bàn giao result hợp lệ cho `009-analysis-result-response-contract` và không expose raw Builder debug payload.

### Key Entities

- **UploadedImage**: multipart image nhận từ app trước khi persistence.
- **BuilderAnalysisRequest**: request nội bộ gửi đến Builder.
- **BuilderAnalysisResult**: kết quả Builder hợp lệ sau normalize/link, trước khi bọc response public cho app.
- **RequestTrace**: metadata truy vết request giữa Backend và Builder.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Ảnh hợp lệ tạo đúng một Builder analysis request.
- **SC-002**: Builder failure ngăn success S3/history persistence.
- **SC-003**: Builder request không chứa `s3_key` hoặc `image_ref`.
- **SC-004**: Invalid file bị từ chối trước downstream call.
- **SC-005**: Builder success result được chuyển sang response contract public riêng.
- **SC-006**: Pytest product extraction pass sau thay đổi.
- **SC-007**: Evidence AI4SE ghi rõ contract API-Builder và kết quả kiểm chứng.

## Assumptions

- Builder reachable qua internal API từ env config.
- Builder chịu trách nhiệm gọi AIaaS, normalize và linking Neo4j.
- Storage/history success path được thực hiện sau Builder success.
