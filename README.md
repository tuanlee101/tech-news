# TechTin 📰 — Tin công nghệ mỗi sáng

Trang tổng hợp tin công nghệ hằng ngày từ báo chí nước ngoài (TechCrunch, The Verge), **tóm tắt sang tiếng Việt** bằng AI.

## Pipeline tự động (cron 8h sáng hằng ngày)

1. `python3 fetcher.py` → kéo RSS mới nhất → `raw.json`
2. Cron job (Hermes) đọc `raw.json` → tóm tắt tiếng Việt (`title_vn`, `summary_vn`) → ghi `data.json`
3. `git push` → GitHub Actions tự deploy lên GitHub Pages

## Chạy thủ công

```bash
python3 fetcher.py   # cập nhật raw.json
```

## Cấu trúc

| File | Vai trò |
|---|---|
| `index.html` | UI tự chứa (dark theme, Be Vietnam Pro), fetch `data.json` |
| `data.json` | Dữ liệu đã tóm tắt tiếng Việt (đầu vào của UI) |
| `raw.json` | Dữ liệu thô từ RSS (bước trung gian) |
| `fetcher.py` | Script kéo RSS (dùng certifi cho SSL, UA trình duyệt) |
| `.github/workflows/deploy.yml` | Auto deploy GitHub Pages khi push main |

## Lưu ý kỹ thuật (đã dính thật)

- Python `/usr/local/bin` thiếu CA cert hệ thống → **bắt buộc** `ssl.create_default_context(cafile=certifi.where())` + truyền `handlers=[HTTPS_HANDLER]` vào `feedparser.parse`, nếu không SSL fail `CERTIFICATE_VERIFY_FAILED`.
- TechCrunch chặn User-Agent `Python-urllib` → phải gửi UA trình duyệt qua `agent=...`.
