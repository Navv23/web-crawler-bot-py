from WebCrawler.Crawlers.webcrawler import WebCrawler

class GoogleSearchScrapper():
    def __init__(self, url):
        self.url = url
        self.crawler = WebCrawler(client='selenium', headless_mode=False)


    def scrape(self):
        page = self.crawler.scrape(self.url)
        return page




if __name__ == '__main__':
    connector = GoogleSearchScrapper(url='https://www.google.com/search?q=python+filetype%3Apdf&rlz=1C1WHAR_enIN1108IN1108&oq=python+filetype%3Apdf&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDk2MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8')
    connector.scrape()