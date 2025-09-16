# 🚀 RPA Job Crawler - Hệ thống Crawl và Phân tích Việc làm RPA

Hệ thống tự động crawl và phân tích thông tin việc làm RPA từ các website tuyển dụng sử dụng Google Gemini AI.

## 📋 Mục lục

- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Tùy chỉnh](#tùy-chỉnh)
- [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
- [Xử lý sự cố](#xử-lý-sự-cố)

## 🛠️ Cài đặt

### Bước 1: Cài đặt Python
Đảm bảo bạn đã cài đặt Python 3.7+ trên máy tính.

### Bước 2: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 3: Kiểm tra cài đặt
```bash
python --version
pip list | grep -E "(requests|beautifulsoup4|google-generativeai|pandas|openpyxl)"
```

## ⚙️ Cấu hình

### 1. Cấu hình API Key Gemini

#### Bước 1: Lấy API Key
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google
3. Tạo API key mới
4. Copy API key

#### Bước 2: Cập nhật API Key
Mở file `crawl.py` và thay đổi dòng 13:

```python
# Tìm dòng này:
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Thay thành:
genai.configure(api_key="AIzaSyB0axHcO5QO82WCJ_lzK73DMCwuFDb434w")  # Thay bằng API key của bạn
```

### 2. Cấu hình danh sách URL

#### Thay đổi danh sách URL
Mở file `crawl.py` và tìm phần `urls = [...]` (dòng 262):

```python
urls = [
    # Thay thế bằng các URL việc làm của bạn
    "https://hrplus.com.vn/jobs/rpa-developer-123",
    "https://topcv.vn/viec-lam/rpa-developer/456",
    "https://vietnamworks.com/rpa-jobs/789",
    # Thêm URL khác...
]
```

#### Lưu ý về URL:
- ✅ **URL hợp lệ**: topcv.vn, vietnamworks.com, itviec.com, jobsgo.vn
- ❌ **URL có vấn đề**: LinkedIn (chặn bot), Facebook (cần đăng nhập)
- ⚠️ **URL cần kiểm tra**: jobstreet.vn (có thể có lỗi SSL)

## 🚀 Sử dụng

### Cấu trúc thư mục
```
RPA job crawl/
├── src/                    # Folder chứa code
│   ├── crawl.py           # Script crawl chính
│   ├── export_to_csv.py   # Script xuất CSV/Excel
│   └── config_example.py  # File cấu hình mẫu
├── result/                # Folder chứa dữ liệu (tự động tạo)
│   ├── jobs_extracted_*.json
│   ├── rpa_jobs_analysis_*.csv
│   └── rpa_jobs_analysis_*.xlsx
└── README.md
```

### Chạy crawl cơ bản
```bash
cd src
python crawl.py
```

### Xuất dữ liệu ra CSV/Excel
```bash
cd src
python export_to_csv.py
```

### Chạy từng bước riêng lẻ
```bash
cd src

# Bước 1: Crawl dữ liệu (lưu vào result/)
python crawl.py

# Bước 2: Xuất CSV/Excel (tự động tìm file JSON mới nhất)
python export_to_csv.py
```

## 📊 Kết quả

Sau khi chạy, tất cả file sẽ được lưu vào folder `result/` với timestamp:

- `jobs_extracted_YYYYMMDD_HHMMSS.json` - Dữ liệu JSON gốc
- `rpa_jobs_analysis_YYYYMMDD_HHMMSS.csv` - File CSV với 46 cột  
- `rpa_jobs_analysis_YYYYMMDD_HHMMSS.xlsx` - File Excel với định dạng đẹp

### Ví dụ file output:
```
result/
├── jobs_extracted_20250917_143022.json
├── rpa_jobs_analysis_20250917_143022.csv
└── rpa_jobs_analysis_20250917_143022.xlsx
```

### Cấu trúc dữ liệu CSV/Excel:

#### Cột theo dõi (5 cột đầu):
1. **STT** - Số thứ tự URL
2. **URL_goc** - Link gốc đầy đủ
3. **Trang_web** - Domain website
4. **Trang_thai** - Trạng thái crawl
5. **Thoi_gian_crawl** - Thời gian crawl

#### Cột thông tin việc làm (41 cột):
6. **Liên hệ** - Email, số điện thoại
7. **Ngày đăng** - Ngày đăng tin
8. **Ngày hết hạn** - Hạn nộp hồ sơ
9. **NĂM** - Năm tuyển dụng
10. **Đơn vị tuyển dụng** - Tên công ty
11. **Lĩnh vực** - Lĩnh vực hoạt động
12. **Vị trí** - Chức danh công việc
13. **Số lượng tuyển** - Số lượng cần tuyển
14. **Nơi làm việc** - Địa điểm
15. **Mô tả** - Mô tả tổng quan
16. **Mô tả yêu cầu công việc** - Yêu cầu chi tiết
17. **Kiến thức** - Kiến thức chung
18. **Kiến thức (chuẩn hoá)** - Kiến thức đã chuẩn hóa
19. **Kiến thức về Hệ điều hành** - Windows, Linux, macOS
20. **Kiến thức về Cơ sở dữ liệu** - MySQL, Oracle, SQL Server
21. **Ngôn ngữ lập trình căn bản** - C, C++, Java
22. **Ngôn ngữ lập trình nâng cao** - .NET, C#, Python, Ruby
23. **Ngôn ngữ lập trình Web** - HTML, CSS, JavaScript, MVC
24. **Tích hợp hệ thống** - Web Services, AWS, JSON, XML, APIs
25. **Công nghệ mới nổi** - AI, Big Data, Blockchain, IoT, ML
26. **Công nghệ tự động hóa** - UiPath, Blue Prism, Automation Anywhere
27. **Quản lý dự án** - Agile, Scrum, Git, Jira
28. **Kỹ năng** - Kỹ năng chung
29. **Kỹ năng (chuẩn hoá)** - Kỹ năng đã chuẩn hóa
30. **Ngoại ngữ tiếng Anh** - Trình độ tiếng Anh
31. **Ngoại ngữ khác** - Nhật, Trung, Pháp
32. **Kỹ năng mềm** - Giao tiếp, làm việc nhóm
33. **Thái độ** - Thái độ chung
34. **Thái độ (chuẩn hoá)** - Thái độ đã chuẩn hóa
35. **Thái độ cụ thể** - Cầu tiến, kỷ luật
36. **Kinh nghiệm** - Kinh nghiệm chung
37. **Kinh nghiệm (chuẩn hoá)** - Kinh nghiệm đã chuẩn hóa
38. **Khác** - Thông tin khác
39. **Khác (chuẩn hoá)** - Thông tin khác đã chuẩn hóa
40. **Bằng cấp đúng chuyên môn** - CNTT, HTTTQL
41. **Chứng chỉ RPA** - UiPath, Blue Prism, Power BI
42. **Kinh nghiệm tự động hóa** - Có/Không
43. **Kinh nghiệm làm việc** - Số năm
44. **Thu nhập & Quyền lợi** - Mức lương và phúc lợi
45. **Thu nhập & quyền lợi (chuẩn hoá)** - Đã chuẩn hóa
46. **Hình thức làm việc** - Full-time, part-time, remote

## 🔧 Tùy chỉnh

### 1. Thay đổi prompt phân tích

Mở file `crawl.py` và tìm hàm `parse_job_with_llm()` (dòng 78):

```python
def parse_job_with_llm(job_text: dict):
    prompt = f"""
    Bạn là một chuyên gia phân tích tin tuyển dụng RPA...
    
    # Thay đổi phần này để điều chỉnh cách phân tích
    Các trường cần trích xuất:
    - "Liên hệ" (string): Thông tin liên hệ...
    - "Ngày đăng" (string): Ngày đăng tin...
    # Thêm hoặc bỏ các trường theo nhu cầu
    
    # Thay đổi yêu cầu phân tích
    QUAN TRỌNG: 
    - Nếu không tìm thấy thông tin cho trường nào, hãy ghi "N/A"
    - Hãy phân tích kỹ và trích xuất thông tin chính xác
    - Trả về JSON với tất cả các trường trên
    """
```

### 2. Thay đổi delay giữa các request

Tìm dòng `time.sleep(1)` trong hàm `process_urls()`:

```python
time.sleep(1)  # Thay đổi số giây (1 = 1 giây)
```

### 3. Thay đổi timeout request

Tìm dòng `timeout=15` trong hàm `fetch_job_page()`:

```python
resp = requests.get(url, headers=headers, timeout=15)  # Thay đổi số giây
```

### 4. Thêm User-Agent khác

Tìm dòng `headers = {"User-Agent": "Mozilla/5.0..."}`:

```python
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
```

## 📈 Trạng thái crawl

### Các trạng thái có thể có:

- **THÀNH_CÔNG** - Crawl và phân tích thành công
- **KHÔNG_TẢI_ĐƯỢC_TRANG** - Lỗi SSL, 403 Forbidden, 410 Gone
- **PHÂN_TÍCH_THẤT_BẠI** - Hết quota API hoặc lỗi phân tích
- **LỖI: [chi tiết]** - Lỗi khác

### Giá trị đặc biệt:

- **N/A** - Không tìm thấy thông tin
- **CRAWL_THẤT_BẠI** - URL không crawl được

## 🐛 Xử lý sự cố

### 1. Lỗi API Key
```
[Gemini API error] 404 models/gemini-1.5-flash is not found
```
**Giải pháp**: Kiểm tra API key và model name

### 2. Lỗi quota
```
[Gemini API error] 429 You exceeded your current quota
```
**Giải pháp**: 
- Đợi reset quota (24h)
- Upgrade lên gói trả phí
- Giảm số lượng URL crawl

### 3. Lỗi SSL
```
[fetch error] SSLError: certificate verify failed
```
**Giải pháp**: 
- Bỏ qua URL có vấn đề SSL
- Thêm proxy nếu cần

### 4. Lỗi 403 Forbidden
```
[fetch error] 403 Client Error: Forbidden
```
**Giải pháp**: 
- Website chặn bot
- Thay đổi User-Agent
- Sử dụng proxy

### 5. Lỗi encoding
```
'charmap' codec can't decode byte
```
**Giải pháp**: 
- Đảm bảo file Python được lưu UTF-8
- Kiểm tra encoding của file CSV

## 📝 Ví dụ sử dụng

### Ví dụ 1: Crawl 5 URL đầu tiên
```python
# Trong crawl.py, thay đổi danh sách URL
urls = [
    "https://topcv.vn/viec-lam/rpa-developer/123",
    "https://vietnamworks.com/rpa-jobs/456",
    "https://itviec.com/viec-lam-it/rpa/789",
    "https://jobsgo.vn/viec-lam/rpa-developer/012",
    "https://hrplus.com.vn/jobs/rpa-dev/345"
]
```

### Ví dụ 2: Thay đổi prompt để phân tích lương
```python
# Trong parse_job_with_llm(), thêm yêu cầu phân tích lương chi tiết
prompt = f"""
...
- "Thu nhập & Quyền lợi" (string): Mức lương cụ thể, VD: "15-25 triệu", "Thỏa thuận", "Upto 40tr"
- "Thu nhập & quyền lợi (chuẩn hoá)" (string): Chuẩn hóa về triệu VND, VD: "15-25tr", "40tr", "Thỏa thuận"
...
"""
```

### Ví dụ 3: Thêm trường mới
```python
# Thêm vào danh sách all_fields trong create_null_record()
all_fields = [
    # ... các trường cũ ...
    "Trạng thái tuyển dụng",  # Thêm trường mới
    "Ưu tiên ứng viên"        # Thêm trường mới
]

# Thêm vào prompt
prompt = f"""
...
- "Trạng thái tuyển dụng" (string): Đang tuyển, Tạm dừng, Đã đủ
- "Ưu tiên ứng viên" (string): Nam, Nữ, Không yêu cầu
...
"""
```

## 🤝 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:

1. **Python version**: `python --version`
2. **Thư viện đã cài**: `pip list`
3. **API key hợp lệ**: Test trên https://aistudio.google.com
4. **URL có thể truy cập**: Mở bằng trình duyệt
5. **File encoding**: UTF-8

## 📄 License

Dự án này được phát hành dưới giấy phép MIT.

---

**🎯 Chúc bạn crawl dữ liệu thành công!**
