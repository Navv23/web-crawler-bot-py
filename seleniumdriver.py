from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumDriver:
    def __init__(self, headless_mode=True, user_agent=None, webdriver_path=None):
        self.headless_mode = headless_mode
        self.user_agent = user_agent
        self.webdriver_path = webdriver_path
        self.driver = None

    def get_driver(self):
        try:
            options = Options()
            if self.headless_mode:
                options.add_argument("--headless")
            if self.user_agent:
                options.add_argument(f"user-agent={self.user_agent}")

            if self.webdriver_path:
                self.driver = webdriver.Chrome(executable_path=self.webdriver_path, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)

            return self.driver
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            return None