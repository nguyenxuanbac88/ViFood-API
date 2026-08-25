# Feature Specification: Tìm Kiếm Và Chi Tiết Tri Thức

**Feature Branch**: `007-search-detail`

**Created**: 2026-08-13

**Status**: Đã duyệt cho quy trình AI4SE

**Input**: Mô tả của người dùng: "ViFood-API cung cấp search/detail public từ Neo4j cho app, map dữ liệu graph sang schema ổn định và không trả raw payload."

## AI4SE Context *(mandatory)*

- **Context Docs**: `Sys-docs/03-api-contracts/mobile-backend-api.md`, `Sys-docs/04-data-models`, `Sys-docs/05-components/backend-api.md`.
- **Agent Rules**: root `AGENTS.md` và `ViFood-API/AGENTS.md`.
- **Spec Kit Artifacts**: `spec.md`, `plan.md`, `tasks.md` trong thư mục này.
- **Codex Skills**: `vifood-kg-linking-check`, `vifood-contract-sync-check`, `vifood-implement-api-change`, `vifood-ai4se-evidence-log`.
- **Codex Role**: đọc ngữ cảnh, đối chiếu contract, sửa router/service/repository/schema/test đúng phạm vi chức năng và không phá ranh giới App -> API -> Builder -> AIaaS.
- **Human Confirmation**: người phát triển review hành vi API, kết quả test và quyết định chấp nhận cuối.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tìm Kiếm Dữ Liệu Tri Thức (Priority: P1)

Người dùng tìm kiếm ingredient, additive, nutrition hoặc product/knowledge item trong app.

**Why this priority**: Search là luồng tra cứu độc lập ngoài scan.

**Independent Test**: Gọi search với keyword tồn tại/rỗng/sai và xác nhận result public có giới hạn.

**Acceptance Scenarios**:

1. **Given** keyword hợp lệ, **When** app gọi search, **Then** Backend trả danh sách public.
2. **Given** keyword rỗng hoặc quá ngắn, **When** gọi search, **Then** Backend trả lỗi validation hoặc empty state hợp lệ.

---

### User Story 2 - Mở Chi Tiết Product Hoặc Knowledge (Priority: P1)

Người dùng mở detail của item tìm kiếm hoặc item từ kết quả scan.

**Why this priority**: Detail cần map đúng id graph sang thông tin public cho app.

**Independent Test**: Mock repository trả detail hợp lệ và missing id để kiểm tra response.

**Acceptance Scenarios**:

1. **Given** id tồn tại trong Neo4j, **When** app gọi detail, **Then** Backend trả schema public.
2. **Given** id không tồn tại, **When** app gọi detail, **Then** Backend trả not_found public.

### Edge Cases

- Request thiếu token hoặc token sai phải trả lỗi public khi endpoint yêu cầu xác thực.
- Response public không chứa stack trace, secret, raw database object hoặc raw internal payload.
- Contract thay đổi phải được đối chiếu với `Sys-docs/03-api-contracts` và client iOS liên quan.
- Không log token, password, API key hoặc ảnh/base64 đầy đủ.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API PHẢI validate query params và limit kết quả search.
- **FR-002**: API PHẢI truy cập Neo4j qua repository/service.
- **FR-003**: API PHẢI map search/detail sang schema public.
- **FR-004**: API PHẢI xử lý empty/missing/not-found ổn định.
- **FR-005**: API KHÔNG ĐƯỢC trả raw Neo4j driver object hoặc debug graph payload.
- **FR-006**: API PHẢI giữ contract khớp DTO iOS khi đổi response.

### Key Entities

- **SearchQuery**: keyword và filter/limit từ app.
- **SearchResultItem**: item rút gọn trong search result.
- **KnowledgeDetail**: detail public theo id.
- **GraphEntityId**: id dùng để truy vấn Neo4j qua Backend API.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Search trả kết quả bounded/paginated khi phù hợp.
- **SC-002**: Empty query được xử lý ổn định.
- **SC-003**: Detail id tồn tại trả schema public.
- **SC-004**: Missing id trả not_found public.
- **SC-005**: Không có raw Neo4j object trong response.
- **SC-006**: Pytest search/detail pass.

## Assumptions

- Neo4j chứa dữ liệu tri thức cần search/detail.
- App chỉ gọi search/detail qua ViFood-API.
- Builder/KC chịu trách nhiệm tạo/liên kết dữ liệu graph, không phải app.
