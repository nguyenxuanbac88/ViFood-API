# Feature Specification: Danh Mục Tri Thức Public

**Feature Branch**: `003-knowledge-catalog`

**Created**: 2026-06-20

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API cung cấp các API đọc danh mục tri thức public từ Neo4j cho app, không trả raw graph hoặc debug payload."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`, `Sys-docs/05-components/knowledge-core.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-implement-api-change`, `vifood-kg-linking-check`, `vifood-contract-sync-check`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Xem Danh Sách Tri Thức (Priority: P1)

App lấy danh sách ingredient, additive, nutrition hoặc nhóm tri thức public để hiển thị.

**Why this priority**: Danh mục tri thức là dữ liệu nền cho search/detail và giải thích kết quả scan.

**Independent Test**: Gọi list endpoint và xác nhận response public có giới hạn/pagination khi phù hợp.

**Acceptance Scenarios**:

1. **Given** dữ liệu Neo4j tồn tại, **When** app gọi list endpoint, **Then** API trả danh sách public đã map.
2. **Given** database rỗng, **When** gọi list, **Then** API trả danh sách rỗng hợp lệ.

---

### User Story 2 - Xem Chi Tiết Tri Thức (Priority: P1)

App mở chi tiết một entity tri thức bằng id public.

**Why this priority**: Detail cần ổn định để người dùng hiểu ingredient/additive/nutrition.

**Independent Test**: Mock repository trả detail và xác nhận API không trả raw Neo4j object.

**Acceptance Scenarios**:

1. **Given** id tồn tại, **When** gọi detail, **Then** API trả schema public.
2. **Given** id không tồn tại, **When** gọi detail, **Then** API trả not_found public.

---

### User Story 3 - Giữ Dữ Liệu Catalog Đúng Ranh Giới (Priority: P3)

Backend chỉ phục vụ dữ liệu curated/imported, không biến dữ liệu scan runtime thành tri thức chuẩn.

**Why this priority**: Tránh làm sai vai trò ViFood-KC và Neo4j.

**Independent Test**: Review route write/admin nếu có và xác nhận không lẫn runtime scan data.

**Acceptance Scenarios**:

1. **Given** request runtime scan, **When** xử lý, **Then** API không ghi trực tiếp thành curated knowledge.
2. **Given** endpoint public, **When** response trả về, **Then** không chứa provenance/debug nội bộ.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI truy cập Neo4j thông qua repository/service, không trả raw driver object.
- **FR-002**: API PHẢI map entity tri thức sang schema public ổn định.
- **FR-003**: API PHẢI xử lý id không tồn tại bằng lỗi public.
- **FR-004**: API PHẢI giới hạn hoặc phân trang list endpoint khi phù hợp.
- **FR-005**: API KHÔNG ĐƯỢC ghi dữ liệu OCR/runtime scan thành tri thức chuẩn.
- **FR-006**: API KHÔNG ĐƯỢC expose provenance/debug nội bộ nếu contract public không định nghĩa.

### Key Entities

- **KnowledgeEntity**: node tri thức public như ingredient/additive/nutrient.
- **KnowledgeListItem**: item rút gọn cho danh sách.
- **KnowledgeDetail**: detail public cho app.
- **CatalogQuery**: tham số lọc/tìm kiếm danh mục.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: List endpoint trả response public ổn định.
- **SC-002**: Detail endpoint map đúng dữ liệu Neo4j.
- **SC-003**: Không có raw Neo4j object trong response.
- **SC-004**: Not-found behavior ổn định.
- **SC-005**: Test catalog/search/detail liên quan pass.
- **SC-006**: Evidence AI4SE ghi rõ ranh giới catalog/runtime.

## Assumptions

- Neo4j là nguồn tri thức chính đã được ViFood-KC import/curate.
- ViFood-API chỉ phục vụ public read hoặc route quản trị có kiểm soát nếu có.
- App không truy cập Neo4j trực tiếp.
