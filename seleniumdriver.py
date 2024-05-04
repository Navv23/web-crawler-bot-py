from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumDriver:
    def __init__(self, headless_mode, user_agent=None):
        self.headless_mode = headless_mode
        self.user_agent = user_agent
        
    def scrape(self, url):
        options = Options()
        if self.headless_mode:
            options.add_argument("--headless")
        if self.user_agent:
            options.add_argument(f"user-agent={self.user_agent}")

        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            content = driver.page_source
            return content
        finally:
            driver.quit()