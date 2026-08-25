# Tasks: Lỗi Public Và Truy Vết Vận Hành

**Input**: Tài liệu thiết kế từ `/specs/008-error-observability/`

**Prerequisites**: `spec.md`, `plan.md`, root `AGENTS.md`, `ViFood-API/AGENTS.md`, Sys-docs liên quan và contract public/internal nếu có.

## Phase 1: AI4SE Context Preparation

**Goal**: Đưa task vào đúng ngữ cảnh trước khi Codex sửa hoặc review code.

- [ ] T001 Đọc docs error/testing/AI4SE verification.
- [ ] T002 Đọc security boundaries trong root và API AGENTS.
- [ ] T003 Chọn skills: `vifood-debug-extraction-flow`, `vifood-secret-security-audit`, `vifood-ai4se-evidence-log`.

## Phase 2: Foundation Review

**Goal**: Xác định router/service/repository/schema/test bị ảnh hưởng và ranh giới kiến trúc cần giữ.

- [ ] T004 Rà soát exception handlers và logging setup.
- [ ] T005 Rà soát public error shape/code list.
- [ ] T006 Rà soát masking/exclusion cho sensitive fields.

## Phase 3: User Stories Implementation And Review

**Goal**: Thực hiện hoặc rà soát từng user story theo thứ tự ưu tiên, mỗi story có kiểm chứng độc lập.

- [ ] T007 [US1] Kiểm tra validation/auth/downstream error mapping.
- [ ] T008 [US1] Kiểm tra request id qua các stage extraction.
- [ ] T009 [US2] Kiểm tra token/secret/full image payload không bị log.
- [ ] T010 [US2] Kiểm tra test hoặc manual checklist cho log correlation.

## Phase 4: Contract And Security Verification

**Goal**: Kiểm tra public contract, downstream boundary và dữ liệu nhạy cảm trước khi chấp nhận.

- [ ] T011 Đối chiếu response/request schema với `Sys-docs/03-api-contracts` và model client liên quan.
- [ ] T012 Kiểm tra không có secret, token, password, raw image/base64, raw MongoDB/Neo4j object hoặc internal payload trong response/log public.
- [ ] T013 Kiểm tra flow không cho App bypass ViFood-API và không cho ViFood-API gọi AIaaS trực tiếp trong luồng chính.

## Phase 5: Verification And Human Confirmation

**Goal**: Kiểm chứng output AI bằng test/build/checklist và chờ người phát triển xác nhận.

- [ ] T014 Chạy `python -m pytest -q` hoặc test subset phù hợp với chức năng.
- [ ] T015 Nếu test không chạy được do môi trường, ghi blocker và dùng checklist review/contract thay thế tạm thời.
- [ ] T016 Người phát triển review hành vi cuối và xác nhận chấp nhận hoặc yêu cầu chỉnh tiếp.
- [ ] T017 Ghi evidence AI4SE: task id, prompt summary, file thay đổi, test/check result, lỗi phát hiện, vòng chỉnh sửa, mức sử dụng output AI và human confirmation.
