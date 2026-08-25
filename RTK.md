# RTK - Rust Token Killer

RTK là công cụ phụ trợ cho Codex/AI agent khi chạy lệnh trong project `ViFood-API`. RTK giúp rút gọn output test, lint, server log và command diagnostics.

RTK không phải dependency runtime của Backend API.

## Rule

Ưu tiên prefix các lệnh shell bằng `rtk`.

```bash
rtk git status
rtk python -m pytest -q
rtk uvicorn app.main:app --reload
```

## Khi Cần Output Đầy Đủ

```bash
rtk proxy python -m pytest -q
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

