from bs4 import BeautifulSoup
import requests
import time
import random

from seleniumdriver import SeleniumDriver
from requestmanager import RequestManager
from logger import configure_logger

request_manager = RequestManager()

class WebCrawler():
    def __init__(self, client, min_delay=1, max_delay=3):
        self.client = client
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.requests_count = 4 

        self.logger = configure_logger()
        
        if self.client == 'selenium':
            self.driver = SeleniumDriver(headless_mode=False).get_driver()

    def scrape(self, url, driver=None, use_session=False):
        try:
            if driver is None:
                driver = self.driver
            if self.client == 'requests':
                content = self.__scrape_with_requests(url, use_session)
            elif self.client == 'selenium':
                content = self.__scrape_with_selenium(url, driver=driver)
            else:
                raise ValueError("Unsupported scraping client")
            
            self.logger.info(f"Scraping completed")
            return content
        except Exception as e:
            self.logger.error(f"Error occurred while scraping: {e}")
            raise

    def __scrape_with_requests(self, url, use_session=False):
        session_used = "Using session" if use_session else "Not using session"
    
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
            
            if use_session:
                session = request_manager.get_session()
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

    def __scrape_with_selenium(self, url, driver):
        try:
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            driver.get(url)

            page = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.logger.info(f"Selenium: Successful request for the URL: {url}")
            return page

        except Exception as e:
            self.logger.error(f"Error occurred while scraping with Selenium: {e}")
            raise
