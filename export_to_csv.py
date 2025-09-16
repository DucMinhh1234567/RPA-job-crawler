import json
import csv
import pandas as pd
from datetime import datetime

def export_to_csv(json_file_path="jobs_extracted.json", csv_file_path="rpa_jobs_analysis.csv"):
    """
    Xuất dữ liệu từ JSON sang CSV với các trường đã định nghĩa
    """
    
    # Đọc dữ liệu từ file JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Lỗi đọc file JSON {json_file_path}")
        return
    
    if not data:
        print("Không có dữ liệu để xuất")
        return
    
    # Định nghĩa các trường theo yêu cầu (thêm các trường theo dõi)
    fieldnames = [
        "STT",
        "URL_goc", 
        "Trang_web",
        "Trang_thai",
        "Thoi_gian_crawl",
        "Liên hệ",
        "Ngày đăng", 
        "Ngày hết hạn",
        "NĂM",
        "Đơn vị tuyển dụng",
        "Lĩnh vực",
        "Vị trí",
        "Số lượng tuyển",
        "Nơi làm việc",
        "Mô tả",
        "Mô tả yêu cầu công việc (chuẩn hoá mô tả,…)",
        "Kiến thức",
        "Kiến thức (chuẩn hoá môn gì,…)",
        "Kiến thức về Hệ điều hành (Windows, Linux, MacOS,…) Unix",
        "Kiến thức về Cơ sở dữ liệu (MySQL, Postgrespl, SQL Server,...) Oracle, MsSQL, APAC, NoSQL",
        "Ngôn ngữ lập trình căn bản (C, C++,...) Java",
        "Ngôn ngữ lập trình nâng cao (.NET, C#, Python,...) Ruby, VBScript, VB.Net VBA",
        "Ngôn ngữ lập trình Web (HTML, DOM, Xpath, CSS, Javascript,...) Ui Element, MVC, ASP.NET",
        "Tích hợp hệ thống (Web Services, AWS, JSON, XML,...) APIs",
        "Một số công nghệ mới nổi (AI, Big Data, Blockchain, RFID, IoT,…) BI Tool, Đám mây(Azure, Máy ảo), ML",
        "Một số công nghệ tự động hóa (Selenium, UiPath, SAP iRPA, RPA, Power Automation, Blue Prism, Automation Anywhere,…)",
        "Quản lý dự án (Agile, Scrum, Git,...) Kanban, BA, BPM, Jira",
        "Kỹ năng",
        "Kỹ năng (chuẩn hoá kỹ năng gì,…)",
        "Ngoại ngữ tiếng Anh",
        "Ngoại ngữ khác (Nhật, Trung, Pháp,...)",
        "Kỹ năng mềm (Giao tiếp, làm việc cộng tác,…)",
        "Thái độ",
        "Thái độ (chuẩn hoá thái độ gì)",
        "Thái độ (có tinh thần cầu tiền, tuân thủ kỷ luật,..)",
        "Kinh nghiệm",
        "Kinh nghiệm (chuẩn hoá kinh nghiệm gì)",
        "Khác",
        "Khác (chuẩn hoá)",
        "Bằng cấp đúng chuyên môn (CNTT, HTTTQL, HTTT,…)",
        "Có chứng chỉ liên quan đến RPA (UiPath, Blue Prism, Power BI,...)",
        "Có kinh nghiệm liên quan đến Tự động hóa",
        "Kinh nghiệm làm việc",
        "Thu nhập & Quyền lợi",
        "Thu nhập & quyền lợi (chuẩn hoá)",
        "Hình thức làm việc"
    ]
    
    # Tạo dữ liệu cho CSV
    csv_data = []
    for job in data:
        row = {}
        for field in fieldnames:
            # Lấy giá trị từ JSON, nếu không có thì ghi N/A
            row[field] = job.get(field, "N/A")
        csv_data.append(row)
    
    # Ghi file CSV
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"✅ Đã xuất {len(csv_data)} bản ghi ra file {csv_file_path}")
        
        # Tạo file Excel nếu có pandas
        try:
            df = pd.DataFrame(csv_data)
            excel_file = csv_file_path.replace('.csv', '.xlsx')
            df.to_excel(excel_file, index=False, engine='openpyxl')
            print(f"✅ Đã xuất file Excel: {excel_file}")
        except ImportError:
            print("💡 Để xuất file Excel, hãy cài: pip install pandas openpyxl")
            
    except Exception as e:
        print(f"❌ Lỗi khi ghi file CSV: {e}")

if __name__ == "__main__":
    export_to_csv()

