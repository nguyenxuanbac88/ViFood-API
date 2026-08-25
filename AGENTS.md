# AGENTS.md - ViFood-API

File này hướng dẫn AI agent khi làm việc trong backend `ViFood-API`. Luôn đọc file root `../AGENTS.md` trước, sau đó đọc file này để nắm quy tắc riêng của Backend API.

## Project Role

`ViFood-API` là Backend API FastAPI trung tâm của hệ thống. Service này là cổng public duy nhất cho app `NutriQuor`, xử lý auth, user profile, nhận ảnh phân tích, gọi Builder, lưu ảnh sau khi thành công, product search/detail và history.

## Architecture Rules

- Backend API là service duy nhất mà app iOS được gọi trực tiếp.
- Backend API không chạy model AI trực tiếp trong luồng phân tích chính.
- Backend API không gọi `LLM-KIE 2 /extract-label` trực tiếp trong flow chính.
- Backend API nhận ảnh từ app, validate ảnh và gửi ảnh/payload ảnh cho `ViFood-KG-Builder /labels/analyze`.
- Backend API chỉ lưu ảnh vào S3/storage sau khi Builder xử lý thành công.
- Backend API tạo `image_ref` sau khi lưu ảnh thành công.
- Backend API lưu lịch sử quét và kết quả phân tích vào MongoDB.
- Backend API truy vấn dữ liệu chính/search/detail từ Neo4j khi phục vụ API public.
- Backend API không trả stack trace, raw internal response, secret hoặc debug payload cho app.

## Data Ownership

- S3/storage: lưu ảnh nhãn gốc sau khi phân tích thành công.
- MongoDB: lưu history record theo user.
- Neo4j: lưu dữ liệu chính, graph, search/detail.
- Builder: tạo response phân tích đã normalize/link graph.
- Backend API: bọc response public trong envelope `{ message, data }` và bổ sung dữ liệu cần thiết như `analysis_id`, `image_ref`.

Không lưu ảnh base64 đầy đủ vào MongoDB. Không xem `image_ref` là dữ liệu AI trích xuất từ nhãn.

## Project Structure

- `app/core`: config, dependencies, security, database clients.
- `app/routers`: FastAPI routes.
- `app/services`: business logic.
- `app/repositories`: data access.
- `app/schemas`: request/response schemas.
- `app/models`: domain models.
- `tests`: pytest tests.

## API Rules

- Public success response dùng envelope `{ "message": "...", "data": ... }`.
- Public error response phải có mã lỗi ổn định và thông tin đã được làm sạch.
- API cần dữ liệu cá nhân phải xác thực bearer token.
- `/products/extract` nhận multipart file từ app.
- Backend API gọi Builder trước khi lưu ảnh vào S3.
- Backend API map lỗi Builder/AIaaS/storage thành lỗi public có kiểm soát.
- Search/detail chỉ đi qua backend, app không truy cập Neo4j.
- History chỉ trả dữ liệu của current user.

## Environment Rules

Secret và endpoint phải lấy từ env/config:

- JWT secret/algorithm/expiry.
- S3 endpoint/access key/secret/bucket.
- Builder base URL và timeout.
- MongoDB URI/database/collection cho history.
- Neo4j URI/user/password cho search/detail.

Không hard-code secret hoặc credential trong code/test/docs.

## RTK Rules

RTK là công cụ phụ trợ bắt buộc để rút gọn output terminal cho Codex/AI agent. RTK không phải dependency runtime của Backend API.

- Luôn luôn prefix lệnh shell bằng `rtk` khi chạy command phục vụ đọc code, tìm kiếm, test, build, lint, log, git hoặc diagnostics.
- Dùng `rtk proxy <cmd>` khi cần output đầy đủ hoặc khi RTK lọc thiếu thông tin cần debug.
- Chỉ được chạy lệnh gốc không qua `rtk` khi RTK lỗi, không hỗ trợ command tương tác/đặc biệt, hoặc cần output thô để debug. Khi fallback, agent phải ghi rõ lý do.

## Testing And Verification

Chạy test backend:

```bash
rtk python -m pytest -q
```

Khi sửa product extraction, kiểm tra:

- Auth/current user.
- File validation.
- Call Builder bằng payload ảnh đúng contract.
- Không lưu S3/MongoDB success khi Builder lỗi.
- S3 upload và `image_ref` sau khi Builder thành công.
- Response envelope.
- MongoDB history save.
- Error mapping.

Khi sửa search/detail, kiểm tra:

- Neo4j repository/service.
- Response public không chứa raw graph/debug không cần thiết.
- `404 not_found` cho entity không tồn tại.

## Do Not

- Không cho app gọi service nội bộ qua backend bypass.
- Không gọi AIaaS trực tiếp thay cho Builder trong flow chính.
- Không upload/lưu ảnh thành công trước khi Builder trả kết quả thành công.
- Không đưa provenance/debug/internal metadata vào response public.
- Không lưu ảnh gốc/base64 đầy đủ vào MongoDB.
- Không sửa test để che lỗi contract.
