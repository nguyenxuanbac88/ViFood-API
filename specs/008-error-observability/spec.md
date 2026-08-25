# Feature Specification: Lỗi Public Và Truy Vết Vận Hành

**Feature Branch**: `008-error-observability`

**Created**: 2026-07-24

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API trả lỗi public ổn định, có request id/tracing cho các stage chính và không log token, secret hoặc ảnh base64 đầy đủ."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/06-ai4se/verification-process.md`, `Sys-docs/08-testing`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-debug-extraction-flow`, `vifood-secret-security-audit`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Nhận Lỗi Public Ổn Định (Priority: P1)

App nhận lỗi có code/message ổn định khi validation, auth hoặc downstream service lỗi.

**Why this priority**: Public error contract giúp app không phụ thuộc lỗi nội bộ của FastAPI, Builder, S3 hoặc database.

**Independent Test**: Gây lỗi validation, unauthorized và downstream failure để xác nhận response có code/message ổn định.

**Acceptance Scenarios**:

1. **Given** validation error, **When** request sai, **Then** API trả lỗi public không có stack trace.
2. **Given** downstream failure, **When** service lỗi, **Then** API map lỗi sang public error có kiểm soát.

---

### User Story 2 - Truy Vết Request Qua Các Stage (Priority: P1)

Developer có thể lần theo request id qua receive image, call Builder, save S3, save history và response.

**Why this priority**: Flow phân tích ảnh đi qua Builder, S3 và MongoDB nên cần truy vết khi lỗi.

**Independent Test**: Gửi request extraction và xác nhận log có cùng request id ở các stage chính.

**Acceptance Scenarios**:

1. **Given** request mới, **When** Backend xử lý, **Then** log chứa request id cho các stage chính.
2. **Given** downstream lỗi, **When** log được ghi, **Then** vẫn có request id để debug.

---

### User Story 3 - Bảo Vệ Dữ Liệu Nhạy Cảm Trong Log (Priority: P1)

Log vận hành không chứa token, secret, password hoặc ảnh base64 đầy đủ.

**Why this priority**: Log là bằng chứng vận hành nhưng không được làm rò rỉ dữ liệu nhạy cảm.

**Independent Test**: Kiểm tra log của request auth/ảnh và xác nhận dữ liệu nhạy cảm được mask hoặc không xuất hiện.

**Acceptance Scenarios**:

1. **Given** request có Authorization header, **When** log request, **Then** token không xuất hiện.
2. **Given** upload ảnh, **When** log payload, **Then** không log full base64/raw image.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI trả lỗi public có code/message ổn định cho validation/auth/downstream errors.
- **FR-002**: API KHÔNG ĐƯỢC trả stack trace, secret, internal URL hoặc raw exception trong public response.
- **FR-003**: API PHẢI log major extraction stages: receive image, call Builder, save S3, save history và response.
- **FR-004**: API PHẢI gắn request id/correlation id khi phù hợp.
- **FR-005**: API PHẢI map Builder, S3, MongoDB và Neo4j errors sang controlled public errors.
- **FR-006**: API KHÔNG ĐƯỢC log token, password, API key hoặc full image/base64 payload.

### Key Entities

- **PublicError**: response lỗi public cho app.
- **RequestId**: correlation id dùng trong log/debug.
- **ExtractionStageLog**: log stage chính trong pipeline.
- **SensitiveDataRule**: quy tắc mask/exclude dữ liệu nhạy cảm.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Validation/auth/downstream lỗi trả public error ổn định.
- **SC-002**: Không có stack trace/internal URL trong public response.
- **SC-003**: Request extraction có request id trong log stage chính.
- **SC-004**: Token/secret/full image payload không xuất hiện trong log.
- **SC-005**: Pytest hoặc checklist observability pass.
- **SC-006**: Evidence AI4SE ghi rõ kiểm chứng bảo mật/log.

## Assumptions

- Một phần logging có thể kiểm chứng bằng test hoặc checklist thủ công nếu môi trường log chưa đầy đủ.
- RTK chỉ là công cụ phụ trợ đọc output, không phải runtime dependency.
- Error contract public cần đồng bộ với iOS UI.
