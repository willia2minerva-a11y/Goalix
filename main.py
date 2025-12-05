import os
import time
import logging
from datetime import datetime
import facebook
import requests
import schedule
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ إعدادات API ============
FB_TOKEN = os.getenv('FB_PAGE_TOKEN')
PAGE_ID = os.getenv('FB_PAGE_ID')
FOOTBALL_KEY = os.getenv('FOOTBALL_API_KEY')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# ============ بوت فيسبوك ============
class FacebookBot:
    def __init__(self):
        self.graph = facebook.GraphAPI(FB_TOKEN)
    
    def post_text(self, text):
        try:
            self.graph.put_object(PAGE_ID, "feed", message=text)
            logger.info(f"✅ نشر: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في النشر: {e}")
            return False
    
    def post_image(self, text, image_path):
        try:
            with open(image_path, 'rb') as img:
                self.graph.put_photo(image=img, message=text)
            logger.info(f"✅ نشر صورة: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في نشر الصورة: {e}")
            return False

# ============ API كرة القدم ============
class FootballAPI:
    def __init__(self):
        self.headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
    
    def get_today_matches(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            params = {'date': today, 'timezone': 'Africa/Algiers'}
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            matches = []
            for match in data.get('response', [])[:5]:
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                time = match['fixture']['date'][11:16]
                league = match['league']['name']
                
                matches.append(f"⚽ {home} 🆚 {away}\n⏰ {time} | {league}")
            
            return matches
        except Exception as e:
            logger.error(f"❌ خطأ في جلب المباريات: {e}")
            return []
    
    def get_live_matches(self):
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            params = {'live': 'all'}
            response = requests.get(url, headers=self.headers, params=params)
            return response.json().get('response', [])
        except Exception as e:
            logger.error(f"❌ خطأ في المباريات الحية: {e}")
            return []

# ============ المهام المجدولة ============
def post_daily_matches():
    """نشر مباريات اليوم"""
    bot = FacebookBot()
    api = FootballAPI()
    
    matches = api.get_today_matches()
    if matches:
        message = "📅 مباريات اليوم:\n\n" + "\n\n".join(matches)
        bot.post_text(message)
    else:
        bot.post_text("📅 لا توجد مباريات اليوم")

def check_live_updates():
    """التحقق من التحديثات الحية"""
    api = FootballAPI()
    bot = FacebookBot()
    
    live_matches = api.get_live_matches()
    for match in live_matches:
        match_id = match['fixture']['id']
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        score = f"{match['goals']['home']}-{match['goals']['away']}"
        
        message = f"🔥 مباراة مباشرة:\n{home} {score} {away}"
        bot.post_text(message)
        break  # نشر مباراة واحدة فقط

# ============ التشغيل الرئيسي ============
def main():
    logger.info("🚀 بدء تشغيل Goalix Bot...")
    
    # جدولة المهام
    schedule.every().day.at("08:00").do(post_daily_matches)
    schedule.every().day.at("18:00").do(post_daily_matches)
    schedule.every(5).minutes.do(check_live_updates)
    
    # اختبار أولي
    bot = FacebookBot()
    bot.post_text("⚽ Goalix Bot يعمل الآن! تابعوا آخر تحديثات الكرة ⚽")
    
    logger.info("✅ البوت يعمل...")
    
    # الحلقة الرئيسية
    while True:
        schedule.run_pending()
        time.sleep(60)
def health():
        return 'OK', 200
    
    return app

# وشغل السيرفر
if __name__ == "__main__":
    # البوت الأساسي في thread منفصل
    import threading
    bot_thread = threading.Thread(target=main, daemon=True)
    bot_thread.start()
    
    # سيرفر ويب بسيط للمنفذ
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=False)

if __name__ == "__main__":
    main()
