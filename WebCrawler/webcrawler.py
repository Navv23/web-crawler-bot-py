from bs4 import BeautifulSoup
import requests
import time
import random

from RequestManager.seleniumdriver import SeleniumDriver
from RequestManager.requestmanager import RequestManager
from Logging.logger import configure_logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

request_manager = RequestManager()

class WebCrawler():
    def __init__(self, client, min_delay=1, max_delay=3, timeout=10, headless_mode=True):
        self.client = client
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.requests_count = 4
        self.headless_mode = headless_mode
        self.logger = configure_logger()
        
        if self.client == 'selenium':
            try:
                self.driver = SeleniumDriver(headless_mode=self.headless_mode).get_driver()
            except Exception as e:
                self.logger.error(f"Error initializing WebDriver: {e}")
                raise

    def scrape(self, url, use_session=False):
        try:
            if self.client == 'requests':
                content = self.__scrape_with_requests(url, use_session)
            elif self.client == 'selenium':
                content = self.__scrape_with_selenium(url)
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

            headers = request_manager.get_headers()
            
            if use_session:
                session = request_manager.get_session()
                response = session.get(url, headers=headers, timeout=self.timeout)
            else:
                response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response and response.status_code == 200:
                self.logger.info(f"{session_used} - Successful request, Request made to {url}, Response code: {response.status_code}")
                if isinstance(response.text, str):
                    return {'status_code':response.status_code, 'content':response.text}
                else:
                    error_message = f"Invalid Response: Response for the URL {url} is not a string"
                    self.logger.error(error_message)
                    return {'status_code': response.status_code, 'content': error_message}
            else:
                if response:
                    self.logger.warning(f"{session_used} - For the {url}, request was not successful. Response code: {response.status_code}")
                    return {'status_code': None, 'content': None}
                
        except requests.RequestException as e:
            self.logger.error(f"Error occurred during request: {e}")
            raise

    def __scrape_with_selenium(self, url):
        try:
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.get(url)

            if "404 - Not Found" in self.driver.title:
                raise ValueError("404 - Not Found")

            page = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "html"))
            )
            if not page:
                raise ValueError("No page content found")

            self.logger.info(f"Selenium: Successful request for the URL: {url}")
            return {'status_code': 200, 'content': BeautifulSoup(self.driver.page_source, 'html.parser')}

        except TimeoutException:
            self.logger.error(f"Timeout occurred while loading the page: {url}")
            return {'status_code': 408, 'content': None}

        except NoSuchElementException as e:
            self.logger.error(f"Element not found while scraping: {e}")
            return {'status_code': 404, 'content': None}

        except Exception as e:
            self.logger.error(f"Unexpected error occurred while scraping with Selenium: {e}")
            return {'status_code': 500, 'content': None}