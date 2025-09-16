import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime

# Sử dụng Google Gemini API:
def call_llm(prompt: str) -> str:
    # TODO: Thay YOUR_GEMINI_API_KEY bằng API key thật của bạn
    # Lấy API key từ: https://aistudio.google.com/app/apikey
    import google.generativeai as genai
    
    # Cấu hình API key
    genai.configure(api_key="Viết key vào đây")
    
    # Khởi tạo model Gemini 1.5 Flash (miễn phí)
    # Thích thì đổi model ở đây
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        # Gửi prompt và nhận response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,  # Để có kết quả nhất quán
                max_output_tokens=8192,  # Tăng limit để xử lý job posting dài
            )
        )
        return response.text
    except Exception as e:
        print(f"[Gemini API error] {e}")
        return None

def fetch_job_page(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fetch error] {url} → {e}")
        return None
    return resp.text

def extract_job_text(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")
    # title
    title = ""
    if soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)
    elif soup.title:
        title = soup.title.get_text(strip=True)

    # try tìm phần mô tả job — heuristic tuỳ trang
    desc = ""
    # một số selector phổ biến
    cands = [
        "div.job-description",
        "div.jd",
        ".job-description",
        "#job-description",
        "section.job-details",
        ".posting-body",
        "div.description"
    ]
    for sel in cands:
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 200:
            desc = el.get_text(separator="\n", strip=True)
            break
    if not desc:
        # fallback: toàn bộ text trang (cắt giới hạn độ dài)
        desc = soup.get_text(separator="\n", strip=True)[:10000]

    return {
        "url": url,
        "title": title,
        "description": desc
    }

def parse_job_with_llm(job_text: dict):
    prompt = f"""
Bạn là một chuyên gia phân tích tin tuyển dụng RPA. Dựa vào tiêu đề và mô tả công việc dưới đây, hãy trích xuất các trường dữ liệu sau và trả về một đối tượng JSON duy nhất.

Các trường cần trích xuất:
- "Liên hệ" (string): Thông tin liên hệ, email, số điện thoại
- "Ngày đăng" (string): Ngày đăng tin tuyển dụng
- "Ngày hết hạn" (string): Ngày hết hạn nộp hồ sơ
- "NĂM" (string): Năm tuyển dụng
- "Đơn vị tuyển dụng" (string): Tên công ty
- "Lĩnh vực" (string): Lĩnh vực hoạt động của công ty
- "Vị trí" (string): Chức danh công việc
- "Số lượng tuyển" (string): Số lượng nhân viên cần tuyển
- "Nơi làm việc" (string): Địa điểm làm việc
- "Mô tả" (string): Mô tả tổng quan về công việc
- "Mô tả yêu cầu công việc (chuẩn hoá mô tả,...)" (string): Yêu cầu chi tiết về công việc
- "Kiến thức" (string): Kiến thức chung cần có
- "Kiến thức (chuẩn hoá môn gì,...)" (string): Kiến thức đã được chuẩn hóa
- "Kiến thức về Hệ điều hành (Windows, Linux, MacOS,…) Unix" (string): Kiến thức về hệ điều hành
- "Kiến thức về Cơ sở dữ liệu (MySQL, Postgrespl, SQL Server,...) Oracle, MsSQL, APAC, NoSQL" (string): Kiến thức về database
- "Ngôn ngữ lập trình căn bản (C, C++,...) Java" (string): Ngôn ngữ lập trình cơ bản
- "Ngôn ngữ lập trình nâng cao (.NET, C#, Python,...) Ruby, VBScript, VB.Net VBA" (string): Ngôn ngữ lập trình nâng cao
- "Ngôn ngữ lập trình Web (HTML, DOM, Xpath, CSS, Javascript,...) Ui Element, MVC, ASP.NET" (string): Công nghệ web
- "Tích hợp hệ thống (Web Services, AWS, JSON, XML,...) APIs" (string): Kiến thức tích hợp hệ thống
- "Một số công nghệ mới nổi (AI, Big Data, Blockchain, RFID, IoT,…) BI Tool, Đám mây(Azure, Máy ảo), ML" (string): Công nghệ mới
- "Một số công nghệ tự động hóa (Selenium, UiPath, SAP iRPA, RPA, Power Automation, Blue Prism, Automation Anywhere,…)" (string): Công nghệ RPA/Automation
- "Quản lý dự án (Agile, Scrum, Git,...) Kanban, BA, BPM, Jira" (string): Kiến thức quản lý dự án
- "Kỹ năng" (string): Kỹ năng chung
- "Kỹ năng (chuẩn hoá kỹ năng gì,…)" (string): Kỹ năng đã chuẩn hóa
- "Ngoại ngữ tiếng Anh" (string): Trình độ tiếng Anh
- "Ngoại ngữ khác (Nhật, Trung, Pháp,...)" (string): Ngoại ngữ khác
- "Kỹ năng mềm (Giao tiếp, làm việc cộng tác,…)" (string): Kỹ năng mềm
- "Thái độ" (string): Thái độ chung
- "Thái độ (chuẩn hoá thái độ gì)" (string): Thái độ đã chuẩn hóa
- "Thái độ (có tinh thần cầu tiền, tuân thủ kỷ luật,..)" (string): Thái độ cụ thể
- "Kinh nghiệm" (string): Kinh nghiệm chung
- "Kinh nghiệm (chuẩn hoá kinh nghiệm gì)" (string): Kinh nghiệm đã chuẩn hóa
- "Khác" (string): Thông tin khác
- "Khác (chuẩn hoá)" (string): Thông tin khác đã chuẩn hóa
- "Bằng cấp đúng chuyên môn (CNTT, HTTTQL, HTTT,…)" (string): Yêu cầu bằng cấp
- "Có chứng chỉ liên quan đến RPA (UiPath, Blue Prism, Power BI,...)" (string): Chứng chỉ RPA
- "Có kinh nghiệm liên quan đến Tự động hóa" (string): Kinh nghiệm automation
- "Kinh nghiệm làm việc" (string): Số năm kinh nghiệm
- "Thu nhập & Quyền lợi" (string): Mức lương và phúc lợi
- "Thu nhập & quyền lợi (chuẩn hoá)" (string): Thu nhập đã chuẩn hóa
- "Hình thức làm việc" (string): Full-time, part-time, remote, hybrid, etc.

Tiêu đề tin tuyển dụng:
{job_text['title']}

Mô tả tin tuyển dụng:
{job_text['description']}

QUAN TRỌNG: 
- Nếu không tìm thấy thông tin cho trường nào, hãy ghi "N/A"
- Hãy phân tích kỹ và trích xuất thông tin chính xác
- Trả về JSON với tất cả các trường trên
- Đối với các trường về công nghệ, hãy liệt kê cụ thể các công nghệ được đề cập
"""
    llm_output = call_llm(prompt)
    if not llm_output:
        print("[LLM parse error] Gemini API returned None")
        return None
    
    # Làm sạch output từ Gemini (loại bỏ markdown formatting)
    cleaned_output = llm_output.strip()
    if cleaned_output.startswith('```json'):
        cleaned_output = cleaned_output[7:]  # Loại bỏ ```json
    if cleaned_output.endswith('```'):
        cleaned_output = cleaned_output[:-3]  # Loại bỏ ```
    cleaned_output = cleaned_output.strip()
    
    try:
        data = json.loads(cleaned_output)
    except Exception as e:
        print("[LLM parse error]", e)
        print("[Raw output preview]", llm_output[:500])
        return None
    return data

def process_urls(urls):
    results = []
    total_urls = len(urls)
    
    print(f"🚀 Bắt đầu crawl {total_urls} URL...")
    
    for index, url in enumerate(urls, 1):
        print(f"\n📊 [{index}/{total_urls}] Đang xử lý: {url[:80]}...")
        
        # Tạo record cơ bản cho mỗi URL
        base_record = {
            "STT": index,
            "URL_goc": url,
            "Trang_web": extract_domain(url),
            "Trang_thai": "",
            "Thoi_gian_crawl": ""
        }
        
        # Thêm timestamp
        from datetime import datetime
        base_record["Thoi_gian_crawl"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Thử crawl URL
            html = fetch_job_page(url)
            if not html:
                print(f"❌ [{index}/{total_urls}] Không thể tải trang")
                base_record["Trang_thai"] = "KHÔNG_TẢI_ĐƯỢC_TRANG"
                # Tạo record với tất cả trường null
                failed_record = create_null_record(base_record)
                results.append(failed_record)
                continue
            
            print(f"✅ [{index}/{total_urls}] Đã tải trang, đang phân tích...")
            jt = extract_job_text(html, url)
            parsed = parse_job_with_llm(jt)
            
            if parsed:
                print(f"🎉 [{index}/{total_urls}] Phân tích thành công!")
                base_record["Trang_thai"] = "THÀNH_CÔNG"
                # Thêm thông tin cơ bản vào parsed data
                parsed.update(base_record)
                results.append(parsed)
            else:
                print(f"❌ [{index}/{total_urls}] Phân tích thất bại")
                base_record["Trang_thai"] = "PHÂN_TÍCH_THẤT_BẠI"
                failed_record = create_null_record(base_record)
                results.append(failed_record)
                
        except Exception as e:
            print(f"❌ [{index}/{total_urls}] Lỗi: {str(e)}")
            base_record["Trang_thai"] = f"LỖI: {str(e)[:50]}"
            failed_record = create_null_record(base_record)
            results.append(failed_record)
        
        time.sleep(1)  # để tránh gửi request quá nhanh
    
    print(f"\n🏁 Hoàn thành! Đã xử lý {len(results)}/{total_urls} URL")
    return results

def extract_domain(url):
    """Trích xuất tên domain từ URL"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace('www.', '')
    except:
        return "unknown"

def create_null_record(base_record):
    """Tạo record với tất cả trường null cho URL thất bại"""
    null_record = base_record.copy()
    
    # Danh sách tất cả các trường cần thiết
    all_fields = [
        "Liên hệ", "Ngày đăng", "Ngày hết hạn", "NĂM", "Đơn vị tuyển dụng", 
        "Lĩnh vực", "Vị trí", "Số lượng tuyển", "Nơi làm việc", "Mô tả",
        "Mô tả yêu cầu công việc (chuẩn hoá mô tả,...)", "Kiến thức", 
        "Kiến thức (chuẩn hoá môn gì,...)", "Kiến thức về Hệ điều hành (Windows, Linux, MacOS,…) Unix",
        "Kiến thức về Cơ sở dữ liệu (MySQL, Postgrespl, SQL Server,...) Oracle, MsSQL, APAC, NoSQL",
        "Ngôn ngữ lập trình căn bản (C, C++,...) Java", 
        "Ngôn ngữ lập trình nâng cao (.NET, C#, Python,...) Ruby, VBScript, VB.Net VBA",
        "Ngôn ngữ lập trình Web (HTML, DOM, Xpath, CSS, Javascript,...) Ui Element, MVC, ASP.NET",
        "Tích hợp hệ thống (Web Services, AWS, JSON, XML,...) APIs",
        "Một số công nghệ mới nổi (AI, Big Data, Blockchain, RFID, IoT,…) BI Tool, Đám mây(Azure, Máy ảo), ML",
        "Một số công nghệ tự động hóa (Selenium, UiPath, SAP iRPA, RPA, Power Automation, Blue Prism, Automation Anywhere,…)",
        "Quản lý dự án (Agile, Scrum, Git,...) Kanban, BA, BPM, Jira", "Kỹ năng",
        "Kỹ năng (chuẩn hoá kỹ năng gì,…)", "Ngoại ngữ tiếng Anh", 
        "Ngoại ngữ khác (Nhật, Trung, Pháp,...)", "Kỹ năng mềm (Giao tiếp, làm việc cộng tác,…)",
        "Thái độ", "Thái độ (chuẩn hoá thái độ gì)", "Thái độ (có tinh thần cầu tiền, tuân thủ kỷ luật,..)",
        "Kinh nghiệm", "Kinh nghiệm (chuẩn hoá kinh nghiệm gì)", "Khác", "Khác (chuẩn hoá)",
        "Bằng cấp đúng chuyên môn (CNTT, HTTTQL, HTTT,…)", 
        "Có chứng chỉ liên quan đến RPA (UiPath, Blue Prism, Power BI,...)",
        "Có kinh nghiệm liên quan đến Tự động hóa", "Kinh nghiệm làm việc",
        "Thu nhập & Quyền lợi", "Thu nhập & quyền lợi (chuẩn hoá)", "Hình thức làm việc"
    ]
    
    # Thêm tất cả trường với giá trị "CRAWL_THẤT_BẠI"
    for field in all_fields:
        null_record[field] = "CRAWL_THẤT_BẠI"
    
    return null_record

def save_results_to_result_folder(data):
    """Lưu kết quả vào folder result/"""
    
    # Tạo folder result nếu chưa có
    result_folder = "../result"
    os.makedirs(result_folder, exist_ok=True)
    
    # Tạo timestamp cho tên file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lưu file JSON
    json_file = os.path.join(result_folder, f"jobs_extracted_{timestamp}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Đã lưu JSON: {json_file}")
    return json_file

if __name__ == "__main__":
    urls = [
        # Thay thế bằng các link
        # ví dụ:
        # "abc.com",
        # "def.com"
        ]
    
    if not urls:
        print("❌ Danh sách URL trống! Vui lòng thêm URL vào danh sách.")
        exit(1)
    
    print(f"🚀 Bắt đầu crawl {len(urls)} URL...")
    data = process_urls(urls)
    
    # Lưu kết quả vào folder result
    json_file = save_results_to_result_folder(data)
    
    print(f"🎉 Hoàn thành! Đã crawl {len(data)} job postings.")
    print(f"📁 Dữ liệu đã được lưu vào folder result/")
    print(f"💡 Chạy 'python export_to_csv.py' để tạo file CSV/Excel")
