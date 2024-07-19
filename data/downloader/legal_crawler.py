import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_legal_texts(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_legal_texts(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = []
    for div in soup.find_all('div', class_='content'):
        text = div.get_text(strip=True)
        texts.append(text)
    return texts

# 示例URL和Headers（请根据实际情况替换）
url = 'https://wenshu.court.gov.cn/List/List?sorttype=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

html = fetch_legal_texts(url, headers)
if html:
    legal_texts = parse_legal_texts(html)
    df = pd.DataFrame(legal_texts, columns=['text'])
    print(df.head())
else:
    print("无法获取法律文本")
