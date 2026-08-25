<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles: Profile scope, traceability and AI4SE workflow clarified
Added sections: AI4SE workflow, verification and evidence requirements
Removed sections: allergies from profile scope
Templates requiring updates: feature specs, implementation plans, tasks
Follow-up tasks: keep specs/evidence synchronized after Backend API changes
-->

# ViFood-API Constitution

ViFood-API là Backend API public của hệ thống ViFood/NutriQuor. Service này nhận request từ app iOS, xử lý xác thực, điều phối phân tích nhãn thực phẩm, lưu ảnh/lịch sử và cung cấp API tra cứu dữ liệu tri thức cho app.

## Core Principles

### I. Backend API Boundary Is Mandatory

App iOS MUST chỉ gọi ViFood-API trong các luồng nghiệp vụ public. ViFood-API MUST là lớp kiểm soát authentication, authorization, request validation, response mapping và public API contract. App không được phụ thuộc trực tiếp vào Builder, AIaaS, Neo4j, S3 hoặc MongoDB.

### II. Product Extraction Flow Is Fixed

Luồng phân tích nhãn MUST đi theo thứ tự: NutriQuor gửi ảnh đến ViFood-API, ViFood-API gửi payload ảnh đến Builder, Builder gọi AIaaS và xử lý tri thức, Builder trả kết quả hợp lệ cho ViFood-API, sau đó ViFood-API mới lưu ảnh vào S3 và lưu lịch sử vào MongoDB. ViFood-API MUST NOT gọi trực tiếp AIaaS trong flow phân tích chính. Builder MUST NOT nhận `s3_key` hoặc `image_ref` làm input phân tích.

### III. Data Ownership Must Stay Explicit

ViFood-API MUST sở hữu user/session, hồ sơ người dùng cơ bản, API contract public, upload ảnh sau phân tích thành công, `image_ref` và lịch sử quét. Neo4j là nguồn dữ liệu tri thức; MongoDB chỉ lưu lịch sử quét của người dùng; S3 chỉ lưu ảnh sau khi phân tích thành công. Response public MUST không trả raw database object, raw graph driver payload hoặc ảnh base64 đầy đủ.

### IV. Profile Scope Is Basic Information Only

Hồ sơ chủ tài khoản và hồ sơ gia đình trong ViFood-API MUST chỉ quản lý thông tin cơ bản. ViFood-API MUST NOT expose public endpoint, profile relationship hoặc app-facing schema cho dị ứng, bệnh nền hoặc mục tiêu sức khỏe trong phạm vi ứng dụng hoàn chỉnh hiện tại.

### V. Contracts And Errors Must Be Stable

Mỗi endpoint public MUST có request/response schema ổn định. Success response SHOULD dùng envelope `{ "message": "...", "data": ... }` theo pattern API hiện có. Error response MUST có mã lỗi/message có kiểm soát, không lộ stack trace, secret, internal URL, prompt, token hoặc raw payload từ service nội bộ.

### VI. Traceability And Verification Are Required

Mỗi thay đổi nghiệp vụ MUST có đường truy vết từ requirement/spec đến plan, task, code và kiểm chứng. Các flow liên quan đến auth, ảnh, Builder, S3, MongoDB hoặc Neo4j MUST có test hoặc checklist kiểm chứng tối thiểu cho luồng thành công và một luồng lỗi đại diện.

## Architecture Boundaries

- NutriQuor là client iOS và không truy cập trực tiếp service nội bộ.
- ViFood-API là Backend API public và là điểm vào duy nhất của app.
- Builder là thành phần backend nội bộ xử lý pipeline tri thức và gọi AIaaS.
- AIaaS là mô hình AI nhận ảnh/payload ảnh từ Builder và trả JSON trích xuất.
- S3 lưu ảnh sau khi Builder xử lý thành công.
- MongoDB lưu lịch sử quét theo user.
- Neo4j lưu dữ liệu tri thức và quan hệ phục vụ search/detail/linking.

## Data Ownership

| Data | Owner |
|---|---|
| Auth/user/session | ViFood-API |
| User profile/basic family info | ViFood-API |
| Public API contract | ViFood-API |
| Label image after successful analysis | ViFood-API writes to S3 |
| `image_ref` | ViFood-API creates after S3 save success |
| Scan history | ViFood-API writes to MongoDB |
| Food knowledge graph | Neo4j accessed through backend services |
| Extraction JSON | AIaaS through Builder |
| Normalization/linking result | Builder |

## Development Workflow

- New work MUST start from a feature folder in `specs/NNN-feature-name`.
- `spec.md` MUST describe AI4SE context, user stories, acceptance scenarios, functional requirements, key entities and measurable success criteria.
- `plan.md` MUST record technical context, architecture decisions, constitution checks, AI4SE execution flow and verification strategy.
- `tasks.md` MUST break implementation into independently testable work items and include context preparation, Codex skill selection, verification, human confirmation and evidence logging.
- Changes to extraction, storage, history, auth, profile, search/detail or public error contract MUST update related Sys-docs when behavior affects thesis-level documentation.
- Mọi task Backend API quan trọng phải đi qua flow AI4SE chuẩn:

```text
Tài liệu ngữ cảnh
  -> AGENTS.md
  -> Spec Kit spec/plan/tasks
  -> Codex Skills
  -> Codex triển khai/rà soát
  -> pytest/contract/manual verification
  -> Con người xác nhận
  -> Ghi evidence
```

## Verification And AI4SE Evidence

- Với thay đổi code, ưu tiên chạy `python -m pytest -q` hoặc test subset phù hợp.
- Với extraction/storage/history, phải kiểm tra Builder success/failure, S3 save, MongoDB history và không gửi `s3_key`/`image_ref` cho Builder.
- Với search/detail/catalog, phải kiểm tra Neo4j mapping và không trả raw graph/debug payload.
- Với auth/profile, phải kiểm tra user scope, token/session và không expose dữ liệu ngoài phạm vi.
- Với mọi task AI4SE quan trọng, phải ghi evidence gồm context, prompt summary, file thay đổi, verification, lỗi phát hiện, chỉnh sửa và xác nhận của con người.

## Governance

This constitution supersedes ad-hoc notes where they conflict with Backend API runtime behavior. Amendments require updating this file, reviewing affected feature specs, and recording the impact in the Sync Impact Report. SemVer applies to governance changes: MAJOR for incompatible principle changes, MINOR for new principles or materially expanded guidance, PATCH for clarifications.

**Version**: 1.1.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-25
