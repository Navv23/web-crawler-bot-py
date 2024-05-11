import logging
import requests
import time
import random
import os

from seleniumdriver import SeleniumDriver
from requestmanager import RequestManager
from bs4 import BeautifulSoup

request_manager = RequestManager()

class WebCrawler(SeleniumDriver):
    def __init__(self, client, webdriver_path=None, use_session=False, min_delay=1, max_delay=3):
        self.client = client
        self.webdriver_path = webdriver_path
        self.use_session = use_session
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.requests_count = 4 

        self.logger = self.__configure_logger()
        
        if self.use_session:
            self.__create_session()
        else:
            self.session = None

        if self.client == 'selenium':
            self.driver = SeleniumDriver(headless_mode=False).get_driver()
        
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
    
    def scrape(self, url):
        try:
            if self.client == 'requests':
                content = self.__scrape_with_requests(url)
            elif self.client == 'selenium':
                content = self.__scrape_with_selenium(url)
            else:
                raise ValueError("Unsupported scraping client")
            
            self.logger.info(f"Scraping completed")
            return content
        except Exception as e:
            self.logger.error(f"Error occurred while scraping: {e}")
            raise

    def __scrape_with_requests(self, url):
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
                response = session.get(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            
            if response and response.status_code == 200:
                self.logger.info(f"{session_used} - Successful request, Request made to {url}, Response code: {response.status_code}")
                if isinstance(response.text, str):
                    return response.text
                else:
                    error_message = f"Invalid Response: Response for the URL {url} is not a string"
                    self.logger.error(error_message)
                    return error_message
            else:
                if response:
                    self.logger.warning(f"{session_used} - For the {url}, request was not successful. Response code: {response.status_code}")
                else:
                    self.logger.warning(f"{session_used} - For the {url}, request was not successful. No response received.")
        except requests.RequestException as e:
            self.logger.error(f"Error occurred during request: {e}")
            raise


    def __scrape_with_selenium(self, url):
        try:
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            self.driver.get(url)

            page = BeautifulSoup(self.driver.page_source, 'html.parser')

            self.logger.info(f"Selenium: Successful request for the URL: {url}")
            return page

        except Exception as e:
            self.logger.error(f"Error occurred while scraping with Selenium: {e}")
            raise

