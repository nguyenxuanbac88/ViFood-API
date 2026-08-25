# Feature Specification: Xác Thực Và Quản Lý Người Dùng

**Feature Branch**: `001-auth-user-management`

**Created**: 2026-06-08

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API cung cấp đăng ký, đăng nhập, refresh token, current user và logout/session behavior cho app NutriQuor thông qua API public."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/06-ai4se`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-secret-security-audit`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Đăng Ký Tài Khoản Mới (Priority: P1)

Người dùng tạo tài khoản để sử dụng các chức năng cá nhân hóa của hệ thống.

**Why this priority**: Auth là điều kiện đầu vào cho scan, history, profile và các API theo user.

**Independent Test**: Gửi request đăng ký hợp lệ và trùng email để xác nhận response public, password không bị trả ra.

**Acceptance Scenarios**:

1. **Given** payload đăng ký hợp lệ, **When** Backend xử lý request, **Then** API tạo user/profile cơ bản và trả envelope public.
2. **Given** email đã tồn tại, **When** người dùng đăng ký lại, **Then** API trả lỗi public ổn định.
3. **Given** payload thiếu field bắt buộc, **When** request được validate, **Then** API từ chối trước khi ghi database.

---

### User Story 2 - Đăng Nhập Và Nhận Token (Priority: P1)

Người dùng đăng nhập bằng thông tin hợp lệ và nhận token để app gọi API bảo vệ.

**Why this priority**: App cần token ổn định để gọi product extraction, history và profile.

**Independent Test**: Gọi login thành công/thất bại và xác nhận response không lộ password hash hoặc secret.

**Acceptance Scenarios**:

1. **Given** credential hợp lệ, **When** login, **Then** API trả access/refresh token theo schema public.
2. **Given** credential sai, **When** login, **Then** API trả lỗi xác thực có kiểm soát.
3. **Given** response login, **When** app decode envelope, **Then** các field bắt buộc khớp contract.

---

### User Story 3 - Refresh Và Current User (Priority: P2)

App làm mới phiên hoặc lấy thông tin current user khi token còn hợp lệ.

**Why this priority**: Giúp app duy trì phiên nhưng vẫn kiểm soát token hết hạn.

**Independent Test**: Mô phỏng token hợp lệ, hết hạn và refresh token sai để kiểm tra dependency current user.

**Acceptance Scenarios**:

1. **Given** access token hợp lệ, **When** gọi current user, **Then** API trả user public của token đó.
2. **Given** refresh token hợp lệ, **When** refresh, **Then** API cấp token mới theo contract.
3. **Given** token sai/hết hạn, **When** gọi API bảo vệ, **Then** API trả unauthorized public.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI cung cấp endpoint đăng ký, đăng nhập, refresh/current user theo contract public.
- **FR-002**: API PHẢI hash password và KHÔNG ĐƯỢC trả password hash ra response.
- **FR-003**: API PHẢI tạo và validate bearer token bằng secret/env config, không hard-code.
- **FR-004**: API PHẢI bọc success response theo envelope public khi pattern endpoint yêu cầu.
- **FR-005**: API PHẢI map lỗi auth thành lỗi public, không trả stack trace hoặc raw exception.
- **FR-006**: API PHẢI bảo đảm dữ liệu current user được scope theo token hiện tại.

### Key Entities

- **UserAccount**: danh tính user public trong hệ thống.
- **AuthToken**: access/refresh token do Backend API cấp.
- **AuthSession**: trạng thái phiên được app sử dụng thông qua token.
- **PublicUserResponse**: DTO không chứa secret/password hash.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Đăng ký hợp lệ tạo user và trả response public.
- **SC-002**: Login hợp lệ trả token theo contract.
- **SC-003**: Credential sai trả lỗi public ổn định.
- **SC-004**: Current user chỉ trả dữ liệu của token hiện tại.
- **SC-005**: Pytest hoặc test auth liên quan pass sau thay đổi.
- **SC-006**: Evidence AI4SE ghi ngữ cảnh, file, kiểm chứng và xác nhận con người.

## Assumptions

- Neo4j/user repository hiện là nguồn lưu user/profile cơ bản.
- JWT secret và thời hạn token lấy từ env/config.
- App chỉ gọi ViFood-API, không gọi database hoặc service nội bộ.
