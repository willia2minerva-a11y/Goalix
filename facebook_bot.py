import facebook
import logging

logger = logging.getLogger(__name__)

class GoalixFacebookBot:
    def __init__(self, page_token, page_id):
        self.graph = facebook.GraphAPI(page_token)
        self.page_id = page_id
    
    def post_match_result(self, home_team, away_team, home_score, away_score, scorer=None):
        """نشر نتيجة مباراة"""
        message = f"🎯 نتيجة المباراة:\n\n"
        message += f"🏠 {home_team}: {home_score}\n"
        message += f"🛫 {away_team}: {away_score}\n"
        
        if scorer:
            message += f"\n⚽ الهداف: {scorer}"
        
        return self.post_text(message)
    
    def post_goal(self, player, team, minute, home_team, away_team):
        """نشر هدف"""
        message = f"⚽⚽⚽ هدف! ⚽⚽⚽\n\n"
        message += f"🎯 {player}\n"
        message += f"👕 {team}\n"
        message += f"⏰ الدقيقة: {minute}\n"
        message += f"\n{home_team} 🆚 {away_team}"
        
        return self.post_text(message)
    
    def post_red_card(self, player, team, minute):
        """نشر بطاقة حمراء"""
        message = f"🟥 بطاقة حمراء! 🟥\n\n"
        message += f"👤 {player}\n"
        message += f"👕 {team}\n"
        message += f"⏰ الدقيقة: {minute}"
        
        return self.post_text(message)
    
    def post_text(self, text):
        """نشر نص عادي"""
        try:
            result = self.graph.put_object(self.page_id, "feed", message=text)
            logger.info(f"✅ تم النشر: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في النشر: {e}")
            return False
    
    def post_with_image(self, text, image_url):
        """نشر مع صورة"""
        try:
            import requests
            from io import BytesIO
            
            response = requests.get(image_url)
            img = BytesIO(response.content)
            
            self.graph.put_photo(image=img, message=text)
            logger.info(f"✅ تم نشر صورة: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في نشر الصورة: {e}")
            return self.post_text(text)  # حاول نشر نص فقط
