# Import the WebCrawler class from your module
from webcrawler import WebCrawler
from selenium.webdriver.common.by import By

#WITH REQUESTS
crawler = WebCrawler(client='requests')
url = 'url'
scraped_content = crawler.scrape(url, use_session=False) #Change use_session to True if needed
print(scraped_content)


#WITH SELENIUM
crawler = WebCrawler(client='selenium')
url = 'url'
scraped_content = crawler.scrape(url)
driver = crawler.driver #THE DRIVER OBJECT INITIALIZED FROM SeleniumDriver CLASS

### --- AN EXAMPLE ON HOW IT CAN BE USED WITH SELENIUM--- ###
channel_name_click = crawler.driver.find_element(By.XPATH, '//yt-formatted-string[@class="style-scope ytd-channel-name"]').click()

print(scraped_content)
