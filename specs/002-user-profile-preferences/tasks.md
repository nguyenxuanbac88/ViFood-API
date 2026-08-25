# Tasks: Hồ Sơ Người Dùng Và Gia Đình

**Input**: Tài liệu thiết kế từ `/specs/002-user-profile-preferences/`

**Prerequisites**: `spec.md`, `plan.md`, root `AGENTS.md`, `ViFood-API/AGENTS.md`, Sys-docs liên quan và contract public/internal nếu có.

## Phase 1: AI4SE Context Preparation

**Goal**: Đưa task vào đúng ngữ cảnh trước khi Codex sửa hoặc review code.

- [ ] T001 Đọc docs profile/family và scope hiện tại trong Sys-docs.
- [ ] T002 Đối chiếu `ViFood-API/AGENTS.md` với root `AGENTS.md` về profile scope.
- [ ] T003 Chọn skills: `vifood-implement-api-change`, `vifood-contract-sync-check`, `vifood-thesis-consistency-check`, `vifood-ai4se-evidence-log`.

## Phase 2: Foundation Review

**Goal**: Xác định router/service/repository/schema/test bị ảnh hưởng và ranh giới kiến trúc cần giữ.

- [ ] T004 Rà soát router/service/repository profile v1.
- [ ] T005 Rà soát public schema profile/family.
- [ ] T006 Tìm và loại bỏ hoặc không expose các field dị ứng, bệnh nền, mục tiêu sức khỏe nếu xuất hiện ở API public.

## Phase 3: User Stories Implementation And Review

**Goal**: Thực hiện hoặc rà soát từng user story theo thứ tự ưu tiên, mỗi story có kiểm chứng độc lập.

- [ ] T007 [US1] Kiểm tra read/update profile theo current user.
- [ ] T008 [US1] Kiểm tra list/create/update/delete family profile cơ bản.
- [ ] T009 [US2] Kiểm tra unauthorized/not-found/cross-user access.

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
