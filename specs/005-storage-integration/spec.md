# Feature Specification: Tích Hợp Lưu Ảnh S3

**Feature Branch**: `005-storage-integration`

**Created**: 2026-08-13

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API lưu ảnh nhãn gốc vào S3/storage chỉ sau khi Builder phân tích thành công và tạo `image_ref` cho response/history."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/backend-builder-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/08-testing/integration-tests.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-debug-extraction-flow`, `vifood-secret-security-audit`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Lưu Ảnh Sau Phân Tích Thành Công (Priority: P1)

Backend lưu ảnh gốc vào S3 sau khi Builder xử lý thành công.

**Why this priority**: Đảm bảo ảnh lưu trữ luôn gắn với kết quả phân tích hợp lệ.

**Independent Test**: Mock Builder success và S3 upload success để xác nhận `image_ref` được tạo.

**Acceptance Scenarios**:

1. **Given** Builder success, **When** storage chạy, **Then** ảnh được lưu vào S3 và sinh `image_ref`.
2. **Given** Builder failure, **When** flow kết thúc, **Then** Backend không upload ảnh lên S3.

---

### User Story 2 - Xử Lý Lỗi Storage (Priority: P1)

Backend xử lý lỗi S3 mà không tạo history thành công sai lệch.

**Why this priority**: Storage failure không được biến thành scan success.

**Independent Test**: Mock S3 upload failure và xác nhận không lưu success history.

**Acceptance Scenarios**:

1. **Given** S3 upload lỗi, **When** Backend lưu ảnh, **Then** API trả lỗi public và không ghi success history.
2. **Given** S3 trả key hợp lệ, **When** Backend map kết quả, **Then** API tạo `image_ref` public.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI upload ảnh gốc chỉ sau Builder success hợp lệ.
- **FR-002**: API PHẢI tạo `image_ref` ổn định sau khi S3 save thành công.
- **FR-003**: API PHẢI dùng env/config cho S3 endpoint/bucket/credential.
- **FR-004**: API KHÔNG ĐƯỢC lưu ảnh base64 đầy đủ vào MongoDB.
- **FR-005**: API KHÔNG ĐƯỢC dùng S3 như nguồn ảnh đầu vào cho Builder trong flow chính.
- **FR-006**: API PHẢI map storage failure thành lỗi public có kiểm soát.

### Key Entities

- **StoredImage**: object ảnh được lưu trong S3 sau phân tích thành công.
- **ImageRef**: tham chiếu ảnh public/internal do Backend tạo.
- **StorageFailure**: lỗi upload/download URL được map sang public error.
- **ScanStorageContext**: metadata user/request dùng để tạo key.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Builder failure tạo 0 lần S3 upload.
- **SC-002**: Builder success + S3 success tạo `image_ref`.
- **SC-003**: S3 failure không tạo success history.
- **SC-004**: MongoDB history chỉ chứa image reference, không chứa ảnh base64.
- **SC-005**: Pytest storage/product/history liên quan pass.
- **SC-006**: Evidence AI4SE ghi rõ thứ tự Builder -> S3 -> MongoDB.

## Assumptions

- S3-compatible storage được cấu hình qua env.
- Ảnh gốc vẫn còn trong memory/request context sau Builder success.
- Download URL nếu có do Backend/S3 service tạo.
