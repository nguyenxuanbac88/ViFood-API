# Feature Specification: Lịch Sử Quét

**Feature Branch**: `006-scan-history`

**Created**: 2026-07-15

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API lưu và truy xuất lịch sử quét theo authenticated user trong MongoDB sau khi phân tích và lưu ảnh thành công."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/08-testing/integration-tests.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-verify-scan-history`, `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Lưu History Sau Scan Thành Công (Priority: P1)

Backend lưu history khi Builder và S3 đều thành công.

**Why this priority**: History là bằng chứng người dùng đã phân tích sản phẩm và là dữ liệu app cần hiển thị lại.

**Independent Test**: Mock Builder success và S3 success, sau đó xác nhận MongoDB có record theo user.

**Acceptance Scenarios**:

1. **Given** analysis success và S3 success, **When** Backend hoàn tất flow, **Then** một history record được lưu cho current user.
2. **Given** analysis hoặc S3 thất bại, **When** flow kết thúc, **Then** không tạo success history.

---

### User Story 2 - Xem Danh Sách History Của Chính Mình (Priority: P1)

Người dùng xem danh sách scan history của tài khoản hiện tại.

**Why this priority**: App cần list history cho màn lịch sử quét.

**Independent Test**: Tạo history cho user A/B, gọi API bằng token user A và xác nhận chỉ thấy record user A.

**Acceptance Scenarios**:

1. **Given** nhiều record của user A, **When** gọi list history, **Then** response trả record của user A theo thứ tự thời gian.
2. **Given** record của user B, **When** user A gọi list, **Then** response không chứa record user B.

---

### User Story 3 - Xem Chi Tiết History (Priority: P2)

Người dùng mở lại chi tiết một lượt scan đã lưu.

**Why this priority**: Detail giúp app hiển thị lại kết quả phân tích cũ.

**Independent Test**: Gọi detail với analysis_id đúng, sai và của user khác.

**Acceptance Scenarios**:

1. **Given** analysis_id thuộc user, **When** gọi detail, **Then** API trả record public.
2. **Given** analysis_id không thuộc user, **When** gọi detail, **Then** API trả not_found/forbidden public.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI lưu scan history chỉ sau Builder success và S3 save success.
- **FR-002**: History document PHẢI có `user_id`, `analysis_id`, `image_ref`, result public, status và timestamp.
- **FR-003**: API PHẢI scope list/detail theo current user.
- **FR-004**: API PHẢI trả history response public không chứa raw MongoDB object.
- **FR-005**: API PHẢI tạo image URL/ref theo storage service khi cần.
- **FR-006**: API KHÔNG ĐƯỢC lưu ảnh base64 đầy đủ vào MongoDB.

### Key Entities

- **ScanHistoryRecord**: MongoDB document cho một lượt scan thành công.
- **AnalysisId**: id định danh lượt phân tích được app dùng để mở detail.
- **HistoryListItem**: item rút gọn trong list history.
- **HistoryDetail**: kết quả phân tích đã lưu cho detail.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: History chỉ lưu khi Builder và S3 thành công.
- **SC-002**: Failure path không tạo success history.
- **SC-003**: List history chỉ trả record của current user.
- **SC-004**: Detail history không trả record của user khác.
- **SC-005**: Pytest scan history pass.
- **SC-006**: Evidence AI4SE ghi rõ MongoDB ownership và user scope.

## Assumptions

- MongoDB là persistence layer cho scan history.
- Neo4j không lưu history theo user.
- S3 tạo `image_ref` trước khi lưu history.
