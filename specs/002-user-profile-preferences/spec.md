# Feature Specification: Hồ Sơ Người Dùng Và Gia Đình

**Feature Branch**: `002-user-profile-preferences`

**Created**: 2026-06-16

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API quản lý hồ sơ cơ bản của chủ tài khoản và hồ sơ gia đình cơ bản, không expose dị ứng, bệnh nền hoặc mục tiêu sức khỏe trong phạm vi hiện tại."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-thesis-consistency-check`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Xem Hồ Sơ Hiện Tại (Priority: P1)

Người dùng đã đăng nhập xem thông tin hồ sơ cơ bản của chính mình.

**Why this priority**: Profile là dữ liệu app cần hiển thị sau đăng nhập.

**Independent Test**: Gọi endpoint profile bằng token user A và xác nhận chỉ nhận dữ liệu user A.

**Acceptance Scenarios**:

1. **Given** token hợp lệ, **When** gọi profile, **Then** API trả hồ sơ cơ bản của current user.
2. **Given** token user A và dữ liệu user B tồn tại, **When** user A gọi profile, **Then** response không chứa dữ liệu user B.

---

### User Story 2 - Cập Nhật Hồ Sơ Cơ Bản (Priority: P1)

Người dùng cập nhật tên hoặc avatar cơ bản qua Backend API.

**Why this priority**: Cho phép app chỉnh thông tin cá nhân mà không vượt scope đề tài.

**Independent Test**: Cập nhật profile hợp lệ rồi đọc lại để xác nhận dữ liệu mới.

**Acceptance Scenarios**:

1. **Given** payload hợp lệ, **When** cập nhật, **Then** API lưu field cơ bản và trả response public.
2. **Given** payload rỗng/sai, **When** cập nhật, **Then** API trả lỗi validation public.

---

### User Story 3 - Quản Lý Hồ Sơ Gia Đình Cơ Bản (Priority: P2)

Người dùng tạo, sửa, xóa hồ sơ gia đình với thông tin cơ bản.

**Why this priority**: Family profile là phần mở rộng người dùng-facing nhưng phải giữ phạm vi cơ bản.

**Independent Test**: Dùng repository/service fake để kiểm tra list/create/update/delete theo current user.

**Acceptance Scenarios**:

1. **Given** current user, **When** tạo family profile, **Then** profile được gắn quyền sở hữu/quyền truy cập.
2. **Given** profile không thuộc user, **When** update/delete, **Then** API từ chối.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI chỉ expose thông tin hồ sơ cơ bản trong profile/family public schema.
- **FR-002**: API KHÔNG ĐƯỢC expose dị ứng, bệnh nền hoặc mục tiêu sức khỏe trong phạm vi hiện tại.
- **FR-003**: API PHẢI scope mọi thao tác profile/family theo current user.
- **FR-004**: API PHẢI validate input trước khi ghi database.
- **FR-005**: API PHẢI map not found/unauthorized thành lỗi public ổn định.
- **FR-006**: API PHẢI giữ response profile không chứa raw database object.

### Key Entities

- **UserProfile**: hồ sơ cơ bản của user hoặc thành viên gia đình.
- **FamilyProfile**: hồ sơ gia đình thuộc quyền truy cập của current user.
- **ProfileUpdateRequest**: payload cập nhật field cơ bản.
- **ProfilePublicResponse**: DTO public cho app.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Current user chỉ xem được profile thuộc quyền của mình.
- **SC-002**: Cập nhật profile hợp lệ được lưu và đọc lại đúng.
- **SC-003**: Không có endpoint/schema public cho dị ứng, bệnh nền hoặc mục tiêu sức khỏe.
- **SC-004**: Lỗi profile được trả dưới dạng public error.
- **SC-005**: Pytest hoặc kiểm chứng service/profile liên quan pass.
- **SC-006**: Evidence AI4SE ghi rõ scope profile cơ bản.

## Assumptions

- Scope profile hiện tại đã chốt là thông tin cơ bản và family cơ bản.
- Các chức năng dị ứng/bệnh nền/mục tiêu sức khỏe không thuộc bản hoàn chỉnh hiện tại.
- Profile repository hiện truy cập Neo4j qua Backend API.
