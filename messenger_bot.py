from flask import Flask, request
import json
import logging

logger = logging.getLogger(__name__)

class GoalixMessengerBot:
    def __init__(self, verify_token, page_token):
        self.verify_token = verify_token
        self.page_token = page_token
        self.app = Flask(__name__)
    
    def setup_routes(self):
        @self.app.route('/webhook', methods=['GET'])
        def verify():
            token = request.args.get('hub.verify_token')
            if token == self.verify_token:
                return request.args.get('hub.challenge')
            return "Invalid verification token"
        
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            data = request.json
            
            if data.get('object') == 'page':
                for entry in data.get('entry', []):
                    for messaging_event in entry.get('messaging', []):
                        self.handle_message(messaging_event)
            
            return "OK"
    
    def handle_message(self, event):
        """معالجة الرسائل الواردة"""
        sender_id = event.get('sender', {}).get('id')
        message_text = event.get('message', {}).get('text', '')
        
        if not message_text:
            return
        
        logger.info(f"📩 رسالة من {sender_id}: {message_text}")
        
        # الردود التلقائية
        responses = {
            'مباريات': '📅 مباريات اليوم:\nسيتم نشرها الساعة 8 صباحاً و6 مساءً',
            'نتيجة': '🎯 آخر النتائج:\nسيتم نشرها الساعة 6 مساءً',
            'أخبار': '📰 أخبار الكرة:\nسيتم نشرها الساعة 12 ظهراً',
            'مساعدة': '⚽ Goalix Bot\n\nالأوامر:\n• مباريات\n• نتيجة\n• أخبار\n• مساعدة'
        }
        
        response = responses.get(message_text, 'أهلاً! أنا Goalix Bot ⚽\nاكتب "مساعدة" للتعرف على الأوامر')
        
        self.send_message(sender_id, response)
    
    def send_message(self, recipient_id, text):
        """إرسال رسالة"""
        import requests
        
        url = f"https://graph.facebook.com/v17.0/me/messages"
        params = {'access_token': self.page_token}
        headers = {'Content-Type': 'application/json'}
        
        data = {
            'recipient': {'id': recipient_id},
            'message': {'text': text}
        }
        
        try:
            response = requests.post(url, params=params, headers=headers, json=data)
            logger.info(f"✅ أرسلت رسالة لـ {recipient_id}")
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الرسالة: {e}")
    
    def start(self, host='0.0.0.0', port=8000):
        """بدء تشغيل سيرفر الويب"""
        self.setup_routes()
        logger.info(f"🌐 بدء سيرفر الويب على {host}:{port}")
        self.app.run(host=host, port=port)
