from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumDriver:
    def __init__(self, headless_mode=True, user_agent=None):
        self.headless_mode = headless_mode
        self.user_agent = user_agent
        self.driver = None

    def get_driver(self):
        try:
            options = Options()
            if self.headless_mode:
                options.add_argument("--headless")
            if self.user_agent:
                options.add_argument(f"user-agent={self.user_agent}")

            self.driver = webdriver.Chrome(options=options)
            return self.driver
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            return None
