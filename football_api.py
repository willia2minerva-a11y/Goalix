import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GoalixFootballAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
    
    def get_todays_fixtures(self):
        """جلب مباريات اليوم"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"{self.base_url}/fixtures"
            params = {
                'date': today,
                'timezone': 'Africa/Algiers'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            fixtures = []
            for fixture in data.get('response', []):
                fixture_data = {
                    'id': fixture['fixture']['id'],
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'home_logo': fixture['teams']['home']['logo'],
                    'away_logo': fixture['teams']['away']['logo'],
                    'time': fixture['fixture']['date'][11:16],
                    'league': fixture['league']['name'],
                    'country': fixture['league']['country'],
                    'status': fixture['fixture']['status']['short']
                }
                fixtures.append(fixture_data)
            
            return fixtures
        except Exception as e:
            logger.error(f"خطأ في جلب المباريات: {e}")
            return []
    
    def get_live_matches(self):
        """جلب المباريات الحية"""
        try:
            url = f"{self.base_url}/fixtures"
            params = {'live': 'all'}
            
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            live_matches = []
            for match in data.get('response', []):
                match_data = {
                    'id': match['fixture']['id'],
                    'home_team': match['teams']['home']['name'],
                    'away_team': match['teams']['away']['name'],
                    'home_score': match['goals']['home'],
                    'away_score': match['goals']['away'],
                    'minute': match['fixture']['status']['elapsed'],
                    'status': match['fixture']['status']['long']
                }
                live_matches.append(match_data)
            
            return live_matches
        except Exception as e:
            logger.error(f"خطأ في جلب المباريات الحية: {e}")
            return []
    
    def get_match_events(self, match_id):
        """جلب أحداث المباراة"""
        try:
            url = f"{self.base_url}/fixtures/events"
            params = {'fixture': match_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            events = []
            for event in data.get('response', []):
                event_data = {
                    'time': event['time']['elapsed'],
                    'type': event['type'],
                    'detail': event.get('detail', ''),
                    'player': event.get('player', {}).get('name', ''),
                    'team': event.get('team', {}).get('name', ''),
                    'assist': event.get('assist', {}).get('name', '')
                }
                events.append(event_data)
            
            return events
        except Exception as e:
            logger.error(f"خطأ في جلب الأحداث: {e}")
            return []
    
    def get_yesterday_results(self):
        """جلب نتائج أمس"""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            url = f"{self.base_url}/fixtures"
            params = {'date': yesterday}
            
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            
            results = []
            for match in data.get('response', []):
                if match['fixture']['status']['short'] == 'FT':
                    result = {
                        'home_team': match['teams']['home']['name'],
                        'away_team': match['teams']['away']['name'],
                        'home_score': match['goals']['home'],
                        'away_score': match['goals']['away'],
                        'league': match['league']['name']
                    }
                    results.append(result)
            
            return results
        except Exception as e:
            logger.error(f"خطأ في جلب النتائج: {e}")
            return []
