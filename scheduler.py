import schedule
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GoalixScheduler:
    def __init__(self, facebook_bot, football_api):
        self.fb_bot = facebook_bot
        self.football_api = football_api
        self.posted_matches = set()
    
    def schedule_daily_tasks(self):
        """جدولة المهام اليومية"""
        # مباريات اليوم الساعة 8 صباحاً
        schedule.every().day.at("08:00").do(self.post_todays_matches)
        
        # أخبار الساعة 12 ظهراً
        schedule.every().day.at("12:00").do(self.post_daily_news)
        
        # نتائج الساعة 6 مساءً
        schedule.every().day.at("18:00").do(self.post_yesterdays_results)
        
        # مباريات الغد الساعة 9 مساءً
        schedule.every().day.at("21:00").do(self.post_tomorrows_matches)
        
        # تحديثات حية كل 5 دقائق
        schedule.every(5).minutes.do(self.check_live_updates)
        
        logger.info("✅ تم جدولة المهام اليومية")
    
    def post_todays_matches(self):
        """نشر مباريات اليوم"""
        logger.info("📅 جاري نشر مباريات اليوم...")
        
        fixtures = self.football_api.get_todays_fixtures()
        if not fixtures:
            self.fb_bot.post_text("📅 لا توجد مباريات اليوم")
            return
        
        message = "📅 مباريات اليوم:\n\n"
        for i, match in enumerate(fixtures[:10], 1):
            message += f"{i}. ⚽ {match['home_team']} 🆚 {match['away_team']}\n"
            message += f"   ⏰ {match['time']} | {match['league']}\n\n"
        
        message += "🔔 تابعوا التحديثات الحية!"
        self.fb_bot.post_text(message)
    
    def post_yesterdays_results(self):
        """نشر نتائج أمس"""
        logger.info("🎯 جاري نشر نتائج الأمس...")
        
        results = self.football_api.get_yesterday_results()
        if not results:
            self.fb_bot.post_text("🎯 لا توجد نتائج للأمس")
            return
        
        message = "🎯 نتائج الأمس:\n\n"
        for i, result in enumerate(results[:10], 1):
            message += f"{i}. {result['home_team']} {result['home_score']}-{result['away_score']} {result['away_team']}\n"
            message += f"   📊 {result['league']}\n\n"
        
        self.fb_bot.post_text(message)
    
    def check_live_updates(self):
        """التحقق من التحديثات الحية"""
        live_matches = self.football_api.get_live_matches()
        
        for match in live_matches:
            match_id = f"{match['home_team']}_{match['away_team']}"
            
            if match_id not in self.posted_matches:
                self.posted_matches.add(match_id)
                
                # نشر بداية المباراة
                message = f"🔥 مباراة مباشرة بدأت!\n\n"
                message += f"🏠 {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']} 🛫\n"
                message += f"⏰ الدقيقة: {match['minute']}\n"
                message += f"📱 تابعوا التحديثات!"
                
                self.fb_bot.post_text(message)
                logger.info(f"✅ نشر بداية مباراة: {match['home_team']} vs {match['away_team']}")
    
    def post_daily_news(self):
        """نشر أخبار اليوم"""
        news_message = "📰 أخبار كرة القدم اليوم:\n\n"
        news_message += "• انتقالات وصفقات جديدة\n"
        news_message += "• إصابات وتحديثات الفرق\n"
        news_message += "• تحضيرات المباريات القادمة\n\n"
        news_message += "تابعونا للمزيد من التفاصيل! ⚽"
        
        self.fb_bot.post_text(news_message)
        logger.info("✅ نشر أخبار اليوم")
    
    def post_tomorrows_matches(self):
        """نشر مباريات الغد"""
        self.fb_bot.post_text("📅 مباريات الغد قريباً... 🔔")
        logger.info("✅ نشر إشعار مباريات الغد")
    
    def start(self):
        """بدء الجدولة"""
        self.schedule_daily_tasks()
        logger.info("🚀 بدء تشغيل الجدولة...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
