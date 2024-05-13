import os
from pathlib import Path  # Import the Path class
from WebCrawler.webcrawler import WebCrawler

class Common():
    def download_file(self, url, download_path):
        self.crawler = WebCrawler(client='requests')
        try:
            response = self.crawler.scrape(url, use_session=False)
            status_code = response.get('status_code')
            content = response.get('content')
            if status_code == 200:
                download_path = Path(download_path)  
                if not download_path.exists():
                    os.makedirs(download_path)
                with open(os.path.join(download_path, url.split('/')[-1]), 'wb') as f:
                    f.write(content.encode('utf-8'))
                print(f"File downloaded successfully: {url}")
            else:
                print(f"Failed to download file. Status Code: {status_code}")
        except Exception as e:
            print(f"Error occurred while downloading file: {e}")
            pass
