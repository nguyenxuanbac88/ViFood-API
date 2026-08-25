# Implementation Plan: Lỗi Public Và Truy Vết Vận Hành

**Branch**: `008-error-observability` | **Date**: 2026-07-24 | **Spec**: `spec.md`

**Input**: Đặc tả chức năng từ `/specs/008-error-observability/spec.md`

## Summary

Chuẩn hóa và kiểm chứng chức năng `Lỗi Public Và Truy Vết Vận Hành` của ViFood-API theo flow AI4SE: bắt đầu từ Sys-docs và AGENTS, dùng Spec Kit artifacts, chọn Codex skills đúng phạm vi, thực hiện hoặc rà soát code Backend API, chạy pytest/contract checks, sau đó chờ người phát triển xác nhận và ghi evidence.

## Technical Context

**Language/Version**: Python/FastAPI  
**Primary Dependencies**: FastAPI, Pydantic, pytest, service/repository layer hiện có  
**Storage**: Theo chức năng: Neo4j cho dữ liệu tri thức/user graph, MongoDB cho scan history, S3 cho ảnh sau phân tích thành công  
**Testing**: `python -m pytest -q`, contract/service tests, integration checklist khi cần  
**Target Platform**: Backend API service  
**Project Type**: web-service  
**Performance Goals**: API phản hồi ổn định, không block quá lâu ngoài timeout downstream đã cấu hình.  
**Constraints**: App chỉ gọi ViFood-API; API không gọi AIaaS trực tiếp trong flow chính; không hard-code secret; không trả internal payload.  
**Scale/Scope**: Một chức năng Backend API có thể kiểm chứng độc lập bằng test hoặc checklist thủ công.

## Constitution Check

- Backend API là public boundary duy nhất cho app: PASS.
- Luồng extraction giữ đúng App -> API -> Builder -> AIaaS -> Builder -> API -> S3/MongoDB khi chức năng liên quan: REQUIRED.
- Data ownership giữa S3, MongoDB, Neo4j và Builder được giữ rõ: REQUIRED.
- Public contract và error response không lộ dữ liệu nội bộ: REQUIRED.
- Task phải truy vết được từ spec/plan/tasks đến test và human confirmation: REQUIRED.

## AI4SE Execution Flow

```text
Sys-docs + root AGENTS.md + ViFood-API/AGENTS.md
  -> spec.md này
  -> plan.md này
  -> tasks.md
  -> Codex Skills được chọn
  -> Codex triển khai/rà soát
  -> pytest/contract/manual verification
  -> con người xác nhận
  -> ghi evidence AI4SE
```

## Verification Strategy

- Chạy `python -m pytest -q` sau thay đổi code Backend API nếu môi trường cho phép.
- Chạy test/contract tập trung vào router, service, repository, schema và error mapping liên quan.
- Với extraction/storage/history, kiểm tra Builder success/failure, S3 save, MongoDB history và không gửi `s3_key` cho Builder.
- Với search/detail/catalog, kiểm tra Neo4j mapping không trả raw graph/debug payload.
- Với auth/profile, kiểm tra user scope, token/session và không lộ secret/password hash.
- Ghi kết quả test, blocker hoặc checklist thủ công vào evidence log.

## Project Structure

```text
app/main.py
app/models/base.py
app/core
app/services/v1/product_service_v1.py
tests
```

**Structure Decision**: Dùng kiến trúc FastAPI hiện có: router nhận request, service xử lý nghiệp vụ, repository truy cập dữ liệu, schema định nghĩa contract public, tests kiểm chứng hành vi. Không thêm bypass từ app đến service nội bộ.

## Complexity Tracking

Không có vi phạm constitution được chấp nhận. Nếu phát hiện lệch flow hoặc contract, phải cập nhật spec/task và sửa code/docs trước khi human confirmation.
