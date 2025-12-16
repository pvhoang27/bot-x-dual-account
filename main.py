import os
import tweepy
import google.generativeai as genai
from dotenv import load_dotenv
import random

# 1. Nạp key (Code này chạy được cả trên máy tính lẫn trên GitHub)
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest') # Dùng bản Flash mới nhất
# model = genai.GenerativeModel('gemini-2.0-flash')
# model = genai.GenerativeModel('gemini-2.0-flash-lite')
# model = genai.GenerativeModel('gemma-3-12b')
def make_news_tweet():
    prompt = """
    Act as a professional Global News Bot.
    Write a short tweet (under 200 characters) in English.
    Topic: Select a random interesting update, event, or fact from ANY field (World News, Business, Technology, Science, Sports, or Entertainment).
    Style: Breaking news style, objective, professional. 
    Requirement: No hashtags. Pure text. Make it sound like a headline.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if len(text) > 280:
            text = text[:275] + "..."
        return text
    except Exception as e:
        print(f"❌ Lỗi Gemini: {e}")
        return None

def post_to_x(content):
    try:
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_TOKEN_SECRET
        )
        response = client.create_tweet(text=content)
        print(f"✅ Đã đăng thành công! ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"❌ Lỗi đăng X: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Bot bắt đầu chạy...")
    tweet = make_news_tweet()
    if tweet:
        print(f"📝 Nội dung: {tweet}")
        post_to_x(tweet)
    else:
        print("⚠️ Không tạo được nội dung.")