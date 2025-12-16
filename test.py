import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("X_API_KEY")
access_token = os.getenv("X_ACCESS_TOKEN")

print("--- KIỂM TRA KEY ---")

if api_key:
    print(f"API Key: Đã đọc được. Độ dài: {len(api_key)} ký tự")
    print(f"3 ký tự đầu: {api_key[:3]}...")
    print(f"3 ký tự cuối: ...{api_key[-3:]}")
    if " " in api_key:
        print("❌ CẢNH BÁO: API Key có chứa dấu cách! Hãy xóa ngay trong file .env")
else:
    print("❌ LỖI: Không tìm thấy API Key.")

if access_token:
    print(f"Access Token: Đã đọc được. Độ dài: {len(access_token)} ký tự")
    # Access token thường bắt đầu bằng ID tài khoản của bạn (số)
    print(f"3 ký tự đầu: {access_token[:3]}...") 
else:
    print("❌ LỖI: Không tìm thấy Access Token.")