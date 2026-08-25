# Tasks: Xác Thực Và Quản Lý Người Dùng

**Input**: Tài liệu thiết kế từ `/specs/001-auth-user-management/`

**Prerequisites**: `spec.md`, `plan.md`, root `AGENTS.md`, `ViFood-API/AGENTS.md`, Sys-docs liên quan và contract public/internal nếu có.

## Phase 1: AI4SE Context Preparation

**Goal**: Đưa task vào đúng ngữ cảnh trước khi Codex sửa hoặc review code.

- [ ] T001 Đọc root `AGENTS.md`, `ViFood-API/AGENTS.md` và docs auth/API liên quan.
- [ ] T002 Rà soát contract mobile-backend cho auth/current user.
- [ ] T003 Chọn skills: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-secret-security-audit`, `vifood-ai4se-evidence-log`.

## Phase 2: Foundation Review

**Goal**: Xác định router/service/repository/schema/test bị ảnh hưởng và ranh giới kiến trúc cần giữ.

- [ ] T004 Rà soát router auth v1 và auth service hiện có.
- [ ] T005 Rà soát JWT/security/dependencies và cách resolve current user.
- [ ] T006 Rà soát schema response để bảo đảm không trả secret/password hash.

## Phase 3: User Stories Implementation And Review

**Goal**: Thực hiện hoặc rà soát từng user story theo thứ tự ưu tiên, mỗi story có kiểm chứng độc lập.

- [ ] T007 [US1] Kiểm tra validate payload đăng ký và lỗi trùng email.
- [ ] T008 [US1] Kiểm tra login success/failure và contract token response.
- [ ] T009 [US2] Kiểm tra refresh/current user với token hợp lệ, hết hạn và sai.

## Phase 4: Contract And Security Verification

**Goal**: Kiểm tra public contract, downstream boundary và dữ liệu nhạy cảm trước khi chấp nhận.

- [ ] T010 Đối chiếu response/request schema với `Sys-docs/03-api-contracts` và model client liên quan.
- [ ] T011 Kiểm tra không có secret, token, password, raw image/base64, raw MongoDB/Neo4j object hoặc internal payload trong response/log public.
- [ ] T012 Kiểm tra flow không cho App bypass ViFood-API và không cho ViFood-API gọi AIaaS trực tiếp trong luồng chính.

## Phase 5: Verification And Human Confirmation

**Goal**: Kiểm chứng output AI bằng test/build/checklist và chờ người phát triển xác nhận.

- [ ] T013 Chạy `python -m pytest -q` hoặc test subset phù hợp với chức năng.
- [ ] T014 Nếu test không chạy được do môi trường, ghi blocker và dùng checklist review/contract thay thế tạm thời.
- [ ] T015 Người phát triển review hành vi cuối và xác nhận chấp nhận hoặc yêu cầu chỉnh tiếp.
- [ ] T016 Ghi evidence AI4SE: task id, prompt summary, file thay đổi, test/check result, lỗi phát hiện, vòng chỉnh sửa, mức sử dụng output AI và human confirmation.
