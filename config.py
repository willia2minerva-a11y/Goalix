import os
from dotenv import load_dotenv

load_dotenv()

# إعدادات فيسبوك
FB_SETTINGS = {
    'page_token': os.getenv('FB_PAGE_TOKEN'),
    'page_id': os.getenv('FB_PAGE_ID'),
    'verify_token': 'goalix_123'
}

# إعدادات API كرة القدم
FOOTBALL_API = {
    'api_key': os.getenv('FOOTBALL_API_KEY'),
    'rapidapi_key': os.getenv('RAPIDAPI_KEY'),
    'rapidapi_host': 'api-football-v1.p.rapidapi.com'
}

# إعدادات التطبيق
APP_SETTINGS = {
    'timezone': 'Africa/Algiers',
    'language': 'ar',
    'post_times': ['08:00', '12:00', '18:00', '21:00']
}

# الدوريات المتابعة
LEAGUES = [
    {'id': 39, 'name': 'الدوري الإنجليزي'},
    {'id': 140, 'name': 'الدوري الإسباني'},
    {'id': 78, 'name': 'الدوري الألماني'},
    {'id': 135, 'name': 'الدوري الإيطالي'},
    {'id': 61, 'name': 'الدوري الفرنسي'},
    {'id': 2, 'name': 'دوري أبطال أوروبا'}
]
