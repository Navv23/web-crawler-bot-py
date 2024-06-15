# Import the WebCrawler class from your module
from Crawlers.webcrawler import WebCrawler
from selenium.webdriver.common.by import By

#---- WITH REQUESTS
crawler = WebCrawler(client='requests', timeout=10) #SET TIMEOUT BASED ON YOUR PAGE WAITIME PREFERENCE
url = 'url'
scraped_content = crawler.scrape(url, use_session=False) #Change use_session to True if needed
print(scraped_content)


#---- WITH SELENIUM
crawler = WebCrawler(client='selenium', headless_mode=False, timeout=10) 
url = 'url'
scraped_content = crawler.scrape(url)
driver = crawler.driver 

### --- AN EXAMPLE ON HOW DRIVER OBJECT CAN BE USED--- ###
channel_name_click = crawler.driver.find_element(By.XPATH, '//yt-formatted-string[@class="style-scope ytd-channel-name"]').click()

print(scraped_content)
