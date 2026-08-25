# ViFood-API Spec Kit

Spec Kit này mô tả các đặc tả phát triển cho `ViFood-API`, Backend API public của hệ thống ViFood/NutriQuor.

## Mục Đích

- Chuyển trách nhiệm của `ViFood-API` thành các spec nhỏ, dễ kiểm chứng.
- Giữ flow runtime đúng với kiến trúc đã chốt.
- Tạo bằng chứng AI4SE theo chuỗi requirement -> spec -> plan -> tasks -> checklist -> implementation.

## Luồng Runtime Cốt Lõi

```text
NutriQuor
  -> ViFood-API / Backend API
  -> ViFood-KG-Builder / Builder
  -> LLM-KIE 2 / AIaaS
  -> Builder normalize/link Neo4j
  -> ViFood-API lưu S3 + MongoDB history
  -> NutriQuor hiển thị
```

## Cấu Trúc Chuẩn

- `.specify/memory/constitution.md`: nguyên tắc phát triển bắt buộc của Backend API.
- `.specify/templates/`: template gốc do GitHub Spec Kit sinh ra.
- `.specify/scripts/`: script hỗ trợ tạo feature, plan và task.
- `.agents/skills/`: kỹ năng Spec Kit cho Codex.
- `specs/`: các feature specification theo dạng `NNN-feature-name`.

## Thứ Tự Đọc

1. `.specify/memory/constitution.md`
2. `specs/001-auth-user-management`
3. `specs/002-user-profile-preferences`
4. `specs/003-knowledge-catalog`
5. `specs/004-product-extraction`
6. `specs/005-storage-integration`
7. `specs/006-scan-history`
8. `specs/007-search-detail`
9. `specs/008-error-observability`

## Quy Ước

- Mỗi folder trong `specs/` đại diện cho một feature/flow lớn.
- `spec.md` mô tả cái cần xây dựng và lý do.
- `plan.md` mô tả cách hiện thực ở mức kỹ thuật.
- `tasks.md` chia nhỏ công việc theo user story.
- Khi thay đổi code, cập nhật spec tương ứng trước hoặc cùng lúc với implementation.
- Profile/preference trong API chỉ bao gồm thông tin cơ bản và dị ứng; không dựng lại bệnh nền hoặc mục tiêu sức khỏe.
