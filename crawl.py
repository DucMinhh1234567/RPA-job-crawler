import requests
from bs4 import BeautifulSoup
import time
import json

# Sử dụng Google Gemini API:
def call_llm(prompt: str) -> str:
    # TODO: Thay YOUR_GEMINI_API_KEY bằng API key thật của bạn
    # Lấy API key từ: https://aistudio.google.com/app/apikey
    import google.generativeai as genai
    
    # Cấu hình API key
    genai.configure(api_key="")
    
    # Khởi tạo model Gemini 1.5 Flash (miễn phí)
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

if __name__ == "__main__":
    urls = [
        # để bạn thay bằng các link cụ thể của bạn
        "https://hrplus.com.vn/jobs/hrp2387-ha-noi-ba-dinh-cong-ty-chuyen-cong-nghe-dan-dau-trong-linh-vuc-so-hoa-co-so-ha-tang-va-cong-trinh-xay-dung-tuyen-dung-rpa-developer-chuyen-vien-phat-trien-tu-dong-hoa-quy-trinh/?utm_source=jobstreetvn&utm_campaign=jobstreetvn&utm_medium=organic",
        "https://www.jobstreet.vn/job/rd/2f78a989928f55ce1e83f988284fb011?abstract_type=original&asp=serp_jdv&disallow=true&fsv=true&sp=serp_jdv&sq=rpa&sr=4&tk=Gl1xlxAspGr7Yx0BnmAs-5NiVAbdO5vzB4V3kx8J9",
        "https://manage.ybox.vn/tuyen-dung/online-hn-cong-ty-sisua-digital-viet-nam-tuyen-dung-nhan-vien-rpa-developer-full-time-2025-68be8259434c085f9875c559",
        "https://vn.joboko.com/viec-lam-online-cong-ty-digisea-tuyen-dung-nhan-vien-rpa-developer-junior-full-time-2025-xvi5868087",
        "https://www.topcv.vn/viec-lam/rpa-developer/1843194.html",
        "https://www.topcv.vn/viec-lam/rpa-developer/1843194.html",
        "https://jobsgo.vn/viec-lam/rpa-developer-automation-anywhere-power-automate-22816915911.html",
        "https://web.facebook.com/groups/vieclamtiengphaphcm/posts/2763191767218568/?_rdc=1&_rdr#",
        "https://www.topcv.vn/viec-lam/rpa-developer/1038884.html?basic-ui=1",
        "https://www.topcv.vn/viec-lam/product-owner-for-api-rpa-crm-automation-remote/1591082.html?ta_source=JobSearchList_LinkDetail&u_sr_id=rXaJzwUy640546xYeHZafmg93aVXa9sQ9rH2qxc0_1758022824",
        "https://www.topcv.vn/viec-lam/rpa-developer-all-level-c-c-python-vb-script-ruby-java-js-net/1871516.html?ta_source=JobSearchList_LinkDetail&u_sr_id=rXaJzwUy640546xYeHZafmg93aVXa9sQ9rH2qxc0_1758022824",
        "https://www.topcv.vn/viec-lam/rpa-developer/1171884.html",
        "https://www.topcv.vn/viec-lam/rpa-developer/1203001.html",
        "https://www.topcv.vn/viec-lam/fresher-junior-rpa-robotic-process-automation-hybrid/1015644.html",
        "https://www.topcv.vn/viec-lam/rpa-developer-dev-robot/286532.html?basic-ui=1",
        "https://itviec.com/viec-lam-it/rpa?job_selected=automation-developer-rpa-developer-python-javascript-cong-ty-cp-cmc-media-5616",
        "https://topdev.vn/viec-lam/rpa-developer-cong-ty-co-phan-cc1-holdings-2054263?src=topdev_search&medium=searchresult",
        "https://topdev.vn/viec-lam/robot-process-automation-developer-cong-ty-tnhh-socotec-viet-nam-2047513?src=topdev_search&medium=searchresult",
        "https://www.vietnamworks.com/rpa-developer-automation-anywhere-power-automate-1936200-jv?source=searchResults&searchType=2&placement=1936200&sortBy=relevance",
        "https://vn.linkedin.com/jobs/view/robot-process-automation-developer-at-socotec-4301121196?position=1&pageNum=0&refId=S7%2FHsKB92ECGzWXsVkdMDw%3D%3D&trackingId=S5K9wzHgYwERPL8mWgyd6Q%3D%3D",
        "https://vn.linkedin.com/jobs/view/rpa-engineer-at-sleek-4289733600?position=2&pageNum=0&refId=S7%2FHsKB92ECGzWXsVkdMDw%3D%3D&trackingId=K%2FFybDKyPrZqQqPvhD0pGQ%3D%3D",
        "https://vn.linkedin.com/jobs/view/remote-junior-full-stack-developer-rpa-web-automation-%24900-at-wao-corporation-4301111931?position=6&pageNum=0&refId=8uWYlk5mb7Yw3Svd6NCTjQ%3D%3D&trackingId=3Znhy4sru74YkYvJ12eRBw%3D%3D",
        "https://www.facebook.com/groups/rpavn/posts/1831525147773883/",
        "https://www.facebook.com/projob.vn/posts/hn-c%C3%B4ng-ty-sisua-digital-vi%E1%BB%87t-nam-tuy%E1%BB%83n-d%E1%BB%A5ng-nh%C3%A2n-vi%C3%AAn-rpa-developer-full-time-2/1095607389351128/",
        "https://www.facebook.com/photo/?fbid=1421807822754221&set=gm.1022520983218784&idorvanity=982148563922693",
        "https://jobs.community.kaplan.com/career/rpa-engineer-robotic-process-automation-engineer/job-descriptions?utm_source=chatgpt.com"
    ]
    data = process_urls(urls)
    # lưu kết quả
    with open("jobs_extracted.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Done. Extracted {len(data)} job postings.")
