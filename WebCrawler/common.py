import os
from WebCrawler.crawler import WebCrawler

class Common():
    def __init__(self):
        self.crawler = WebCrawler(client='requests')

    def download_file(self, url, download_path):
        try: 
            response = self.crawler.scrape(url)
            status_code = response.get('status_code')
            content = response.get('content')
            
            if status_code == 200:
                if os.path.exists(download_path) and not os.path.isdir(download_path):
                    print(f"Error: Download path '{download_path}' exists and is not a directory.")
                    return None
                
                os.makedirs(download_path, exist_ok=True)
                file_name = url.split('/')[-1]
                file_path = os.path.join(download_path, file_name)
                
                with open(file_path, 'wb') as f:
                    f.write(content.encode('utf-8'))  # Encode content to bytes
                print(f"File downloaded successfully: {file_path}")
                return file_path
            else:
                print(f"Failed to download file. Status Code: {status_code}")
                return None
        
        except Exception as e:
            print(f"Error occurred while downloading file: {e}")
            return None
