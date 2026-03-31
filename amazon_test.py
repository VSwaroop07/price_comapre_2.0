import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

API_KEY = "0d3c058d03367f0dd63047cb4d8454ff"

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'in'}
    return "https://api.scraperapi.com/?" + urllib.parse.urlencode(payload)

url_link_am = "https://www.amazon.in/s?k=iphone+13"

try:
    print("Fetching Amazon data via ScraperAPI...")
    response_am = requests.get(get_scraperapi_url(url_link_am), timeout=30)
    print("Status:", response_am.status_code)
    
    if response_am.status_code == 200:
        soup_am = BeautifulSoup(response_am.text, 'html.parser')
        items = soup_am.find_all('div', {'data-component-type': 's-search-result'})
        print(f"Items found: {len(items)}")
        
        if items:
            item = items[0]
            # Write the html of the first item to a log file
            with open('amazon_item.html', 'w', encoding='utf-8') as f:
                f.write(item.prettify())
            
            # Print h2, h3, spans that might contain titles
            print("--- H2 Elements ---")
            for h2 in item.find_all('h2'):
                print("H2:", h2.text.strip(), "| Class:", h2.get('class'))
                
            print("--- Span Elements (longer text) ---")
            for span in item.find_all('span', class_=lambda x: x and isinstance(x, list) and ('a-text-normal' in x or 'a-size-medium' in x or 'a-size-base-plus' in x)):
                print("Span:", span.text.strip(), "| Class:", span.get('class'))
except Exception as e:
    print("Error:", e)
