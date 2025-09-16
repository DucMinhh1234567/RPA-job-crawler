# -*- coding: utf-8 -*-
"""
File cấu hình mẫu - Copy và đổi tên thành config.py để sử dụng
"""

# =============================================================================
# CẤU HÌNH API
# =============================================================================

# Google Gemini API Key
# Lấy từ: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Model Gemini sử dụng
GEMINI_MODEL = "gemini-1.5-flash"  # Miễn phí
# GEMINI_MODEL = "gemini-1.5-pro"  # Trả phí, chất lượng cao hơn

# Cấu hình generation
GEMINI_TEMPERATURE = 0.0  # 0.0 = nhất quán, 1.0 = sáng tạo
GEMINI_MAX_TOKENS = 8192  # Giới hạn token output

# =============================================================================
# CẤU HÌNH CRAWL
# =============================================================================

# Delay giữa các request (giây)
REQUEST_DELAY = 1

# Timeout cho mỗi request (giây)
REQUEST_TIMEOUT = 15

# User-Agent cho requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Số lần retry khi request thất bại
MAX_RETRIES = 3

# =============================================================================
# DANH SÁCH URL MẪU
# =============================================================================

# Danh sách URL việc làm RPA mẫu
SAMPLE_URLS = [
    "https://hrplus.com.vn/jobs/rpa-developer-123",
    "https://topcv.vn/viec-lam/rpa-developer/456",
    "https://vietnamworks.com/rpa-jobs/789",
    "https://itviec.com/viec-lam-it/rpa/012",
    "https://jobsgo.vn/viec-lam/rpa-developer/345"
]

# =============================================================================
# CẤU HÌNH PROMPT
# =============================================================================

# Prompt mẫu cho phân tích việc làm
SAMPLE_PROMPT = """
Bạn là một chuyên gia phân tích tin tuyển dụng RPA. Dựa vào tiêu đề và mô tả công việc dưới đây, hãy trích xuất các trường dữ liệu sau và trả về một đối tượng JSON duy nhất.

Các trường cần trích xuất:
- "Liên hệ" (string): Thông tin liên hệ, email, số điện thoại
- "Đơn vị tuyển dụng" (string): Tên công ty
- "Vị trí" (string): Chức danh công việc
- "Nơi làm việc" (string): Địa điểm làm việc
- "Mô tả" (string): Mô tả tổng quan về công việc
- "Thu nhập & Quyền lợi" (string): Mức lương và phúc lợi
- "Hình thức làm việc" (string): Full-time, part-time, remote, hybrid, etc.

Tiêu đề tin tuyển dụng:
{title}

Mô tả tin tuyển dụng:
{description}

QUAN TRỌNG: 
- Nếu không tìm thấy thông tin cho trường nào, hãy ghi "N/A"
- Trả về JSON hợp lệ
- Phân tích chính xác và chi tiết
"""

# =============================================================================
# CẤU HÌNH XUẤT DỮ LIỆU
# =============================================================================

# Tên file output
OUTPUT_JSON = "jobs_extracted.json"
OUTPUT_CSV = "rpa_jobs_analysis.csv"
OUTPUT_EXCEL = "rpa_jobs_analysis.xlsx"

# Encoding cho file
FILE_ENCODING = "utf-8"

# Có tạo file Excel không
CREATE_EXCEL = True

# Có tạo sheet thống kê không
CREATE_SUMMARY_SHEET = True

# =============================================================================
# CẤU HÌNH LOGGING
# =============================================================================

# Có hiển thị log chi tiết không
VERBOSE_LOGGING = True

# Có lưu log vào file không
SAVE_LOG_TO_FILE = False
LOG_FILE = "crawl_log.txt"

# =============================================================================
# CÁCH SỬ DỤNG
# =============================================================================

"""
1. Copy file này và đổi tên thành config.py
2. Điền API key của bạn vào GEMINI_API_KEY
3. Thay đổi danh sách URL trong SAMPLE_URLS
4. Tùy chỉnh các cấu hình khác theo nhu cầu
5. Import vào crawl.py:

from config import *

# Sử dụng trong code:
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)
urls = SAMPLE_URLS
"""
