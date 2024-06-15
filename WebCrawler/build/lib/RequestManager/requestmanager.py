from fake_useragent import UserAgent
from Configs.settings import BROWSERS, PLATFORMS
import requests

class RequestManager:
    def __init__(self):
        self.ua = UserAgent(browsers=BROWSERS, platforms=PLATFORMS)

    def rotate_user_agent(self):
        return self.ua.random

    def get_headers(self):
        headers = {
            'User-Agent': self.rotate_user_agent(),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': '',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers
    
    def get_session(self):
        headers = self.get_headers()
        session = requests.Session()
        session.headers.update(headers)
        return session