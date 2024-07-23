import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import json

class WebScraper:
    def __init__(self):
        self.url = 'https://www.blocktempo.com/2024/'
        self.title_class_name = 'jeg_post_title'
        self.date_class_name = 'fa fa-clock-o'
        self.content_class_name = 'intro_quote'
        self.container_class_name = 'jeg_posts jeg_load_more_flag'
        self.titles = []
        self.links = []

    def fetch_links_and_titles(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:  # 確保狀態碼為200
                soup = BeautifulSoup(response.text, 'html.parser')
                today = datetime.now().strftime("%Y-%m-%d")  # 當前日期
                
                # 查找指定框架
                container = soup.find(class_=self.container_class_name)
                if container:
                    # 在框架內查找符合條件的日期
                    date_elements = container.find_all(class_=self.date_class_name)
                    for element in date_elements:
                        element = element.find_parent('a')
                        date_text = element.get_text(strip=True)
                        if date_text == today:
                            if element and element['href']:
                                self.links.append(element['href'])
            else:
                print(f"Error: Received status code {response.status_code} from {self.url}")
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")

    def fetch_details_from_links(self):
        detailed_data = []
        for link in self.links:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 抓取標題
                    title_element = soup.find(class_=self.title_class_name)
                    title = title_element.get_text(strip=True) if title_element else 'No title found'
                    
                    # 抓取內容
                    
                    # content_elements = soup.find(class_=self.content_class_name).find_all(['p', 'h3'])
                    # content = [element.get_text(strip=True) for element in content_elements]
                    
                    content = soup.find('p',class_ = self.content_class_name)
                    content = content.get_text(strip=True) if content else 'No content found'
                    detailed_data.append({
                        'url': link,
                        'title': title,
                        'content': content
                    })
                else:
                    print(f"Error: Received status code {response.status_code} from {link}")
            except requests.RequestException as e:
                print(f"Error fetching {link}: {e}")
        
        return detailed_data

    def save_to_csv(self, filename='scraped_data.csv'):
        data = self.fetch_details_from_links()
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Title', 'Content'])
            for item in data:
                content = ' '.join(item['content'])
                writer.writerow([item['url'], item['title'], content])

    def to_json(self):
        data = self.fetch_details_from_links()
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        return json_data

# 使用範例
if __name__ == "__main__":
    scraper = WebScraper()
    scraper.fetch_links_and_titles()
    
    # 儲存為 CSV 檔案
    scraper.save_to_csv()
    
    # 取得 JSON 格式的資料
    json_data = scraper.to_json()
