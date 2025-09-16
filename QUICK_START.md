# ⚡ Hướng dẫn nhanh - RPA Job Crawler

## 🚀 Chạy ngay trong 3 bước

### Bước 1: Cài đặt
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình API Key
Mở file `src/crawl.py`, tìm dòng 13 và thay API key:
```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```

### Bước 3: Chạy
```bash
cd src
python run_full_process.py
```

**Hoặc chạy từng bước:**
```bash
cd src
python crawl.py          # Crawl dữ liệu
python export_to_csv.py  # Xuất CSV/Excel
```

## 🔧 Tùy chỉnh nhanh

### Thay danh sách URL
Mở `src/crawl.py`, tìm `urls = [...]` và thay bằng URL của bạn.

### Thay prompt phân tích
Mở `src/crawl.py`, tìm hàm `parse_job_with_llm()` và thay đổi prompt.

## 📊 Kết quả
Tất cả file được lưu vào folder `result/`:
- `jobs_extracted_YYYYMMDD_HHMMSS.json` - Dữ liệu JSON
- `rpa_jobs_analysis_YYYYMMDD_HHMMSS.csv` - File CSV
- `rpa_jobs_analysis_YYYYMMDD_HHMMSS.xlsx` - File Excel

## 🆘 Lỗi thường gặp

| Lỗi | Giải pháp |
|-----|-----------|
| 429 quota exceeded | Đợi 24h hoặc upgrade API |
| 403 Forbidden | URL bị chặn, thử URL khác |
| SSL Error | Bỏ qua URL có vấn đề SSL |
| Module not found | Chạy `pip install -r requirements.txt` |

---
**📖 Đọc README.md để biết chi tiết hơn!**
