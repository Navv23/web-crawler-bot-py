import logging
import requests
from requests.adapters import HTTPAdapter
import time
import random
import os

from urllib3 import Retry
from seleniumdriver import SeleniumDriver
from requestmanager import RequestManager

request_manager = RequestManager()

class WebCrawler:
    def __init__(self, url, client, use_session=False, min_delay=1, max_delay=3):
        self.url = url
        self.client = client
        self.use_session = use_session
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.requests_count = 4 

        self.logger = self.__configure_logger()

        if self.use_session:
            self.__create_session()
        else:
            self.session = None

    def __configure_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        project_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(project_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, 'scraping.log')
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    def scrape_page(self):
        try:
            if self.client == 'requests':
                content = self.__scrape_with_requests()
            elif self.client == 'selenium':
                content = self.__scrape_with_selenium()
            else:
                raise ValueError("Unsupported scraping client")
            
            self.logger.info(f"Scraping completed for URL: {self.url}")
            return content
        except Exception as e:
            self.logger.error(f"Error occurred while scraping: {e}")
            raise

    def __scrape_with_requests(self):
        session_used = "Using session" if self.use_session else "Not using session"
        
        try:
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            self.requests_count += 1

            if self.requests_count > 1 and self.requests_count % 4 == 0:
                extra_delay = random.uniform(1, 4)
                self.logger.info(f"Pausing for additional {extra_delay} seconds for politeness")
                time.sleep(extra_delay)

            user_agent = request_manager.rotate_user_agent()
            headers = {'User-Agent': user_agent}
            
            if self.use_session:
                session = self.session
                response = session.get(self.url, headers=headers)
            else:
                response = requests.get(self.url, headers=headers)
            
            if response and response.status_code == 200:
                self.logger.info(f"{session_used} - Successful request, Request made to {self.url}, Response code: {response.status_code}")
                if isinstance(response.text, str):
                    return response.text
                else:
                    error_message = f"Invalid Response: Response for the URL {self.url} is not a string"
                    self.logger.error(error_message)
                    return error_message
            else:
                if response:
                    self.logger.warning(f"{session_used} - For the {self.url}, request was not successful. Response code: {response.status_code}")
                else:
                    self.logger.warning(f"{session_used} - For the {self.url}, request was not successful. No response received.")
        except requests.RequestException as e:
            self.logger.error(f"Error occurred during request: {e}")
            raise

    def __scrape_with_selenium(self):
        try:
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)

            user_agent = request_manager.rotate_user_agent()

            scrapper = SeleniumDriver(headless_mode=True, user_agent=user_agent)
            
            content = scrapper.scrape(self.url)

            if isinstance(content, str):
                self.logger.info(f"Selenium: Successful request for the url: {self.url}")
                return content
            else:
                error_message = "Invalid Response: Response is not a string"
                self.logger.error(error_message)
                return error_message
        except Exception as e:
            self.logger.error(f"Error occurred while scraping with Selenium: {e}")
            raise

    def __create_session(self):
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504, 429])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

# Example usage for Selenium:
# url = "https://www.youtube.com/watch?v=qCuPvl1kIro"
# scrapper = WebCrawler(url, 'selenium')
# try:
#     content = scrapper.scrape_page()
#     print(content)
# except Exception as e:
#     print(e)

# Example usage for Requests:
# url = "https://www.youtube.com/watch?v=qCuPvl1kIro"
# scrapper = WebCrawler(url, 'requests', use_session=False)
# try:
#     content = scrapper.scrape_page()
#     print(content)
# except Exception as e:
#     print(e)