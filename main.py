import os
import time
import tweepy
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Nạp key
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"👉 5 ký tự cuối của Key đang dùng: ...{GEMINI_API_KEY[-5:]}")

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# --- CẤU HÌNH TÀI KHOẢN VÀ CHỮ KÝ RIÊNG ---
ACCOUNTS = [
    {
        "name": "Account 1",
        "api_key": os.getenv("X_API_KEY_1"),
        "api_secret": os.getenv("X_API_SECRET_1"),
        "access_token": os.getenv("X_ACCESS_TOKEN_1"),
        "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET_1"),
        # Nội dung thêm vào để khác biệt
        "signature": "\n\n hn fdsssd .\n#BreakingNews 6868 #HN #GlobalUpdate fdsfd" 
    },
    {
        "name": "Account 2",
        "api_key": os.getenv("X_API_KEY_2"),
        "api_secret": os.getenv("X_API_SECRET_2"),
        "access_token": os.getenv("X_ACCESS_TOKEN_2"),
        "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET_2"),
        # Nội dung thêm vào để khác biệt
        "signature": "\n\n ====) Misfdfdsfds .\n#DailyNews sdfd #MIMIMI #TechWorld tyualdmsa qnfdskfdjdkfdsksfksdf"
    }
]

def make_news_tweet():
    # Mình yêu cầu Gemini viết ngắn hơn xíu (tầm 180 ký tự) để chừa chỗ cho chữ ký thêm vào
    prompt = """
    Act as a professional Global News Bot.
    Write a short tweet (under 180 characters) in English.
    Topic: Select a random interesting update, event, or fact from ANY field (World News, Business, Technology, Science, Sports, or Entertainment).
    Style: Breaking news style, objective, professional. 
    Requirement: No hashtags in this part. Pure text. Make it sound like a headline.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        return text
    except Exception as e:
        print(f"❌ Lỗi Gemini: {e}")
        return None

def post_to_x(content, creds):
    try:
        client = tweepy.Client(
            consumer_key=creds["api_key"],
            consumer_secret=creds["api_secret"],
            access_token=creds["access_token"],
            access_token_secret=creds["access_token_secret"]
        )
        # Tạo nội dung cuối cùng = Nội dung gốc + Chữ ký riêng
        final_content = content + creds["signature"]
        
        response = client.create_tweet(text=final_content)
        print(f"✅ [{creds['name']}] Đã đăng: {final_content}")
        print(f"   -> Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"❌ [{creds['name']}] Lỗi đăng X: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Bot khởi động: 1 Prompt -> Đăng nhiều Acc (Kèm chữ ký riêng)...")

    # 1. Gọi Gemini MỘT LẦN DUY NHẤT (Tiết kiệm quota)
    print("⏳ Đang request nội dung gốc từ Gemini...")
    base_content = make_news_tweet()

    if base_content:
        print(f"📝 Nội dung gốc: {base_content}\n")
        
        # 2. Vòng lặp đăng bài
        for i, acc in enumerate(ACCOUNTS):
            print(f"--- Bắt đầu xử lý: {acc['name']} ---")
            
            # Đăng bài (Hàm này sẽ tự ghép chữ ký Ares/Chris vào)
            post_to_x(base_content, acc)
            
            # 3. Logic ngủ 5 phút (Chỉ ngủ nếu chưa phải acc cuối cùng)
            if i < len(ACCOUNTS) - 1:
                print("💤 Đang ngủ 5 phút (300s) để tránh spam...")
                time.sleep(5) # 300 giây
                print("⏰ Dậy rồi! Tiếp tục làm việc.\n")
            else:
                print("🏁 Hoàn tất danh sách!")
                
    else:
        print("⚠️ Không lấy được nội dung từ Gemini. Hủy chu trình.")