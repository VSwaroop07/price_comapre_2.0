import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

API_KEY = "0d3c058d03367f0dd63047cb4d8454ff"
search = "iphone 13"

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'in'}
    return "https://api.scraperapi.com/?" + urllib.parse.urlencode(payload)

print("--- AMAZON HTML DUMP ---")
url_link_am = "https://www.amazon.in/s?k=" + search.replace(' ', '+')
response_am = requests.get(get_scraperapi_url(url_link_am))
if response_am.status_code == 200:
    soup_am = BeautifulSoup(response_am.text, 'html.parser')
    items = soup_am.find_all('div', {'data-component-type': 's-search-result'})
    
    print("Found items:", len(items))
    for item in items[:2]:
        name_elem = item.find('h2')
        name = name_elem.text.strip() if name_elem else "None"
        
        price_elem = item.find('span', class_='a-price-whole')
        price = price_elem.text.strip().replace(',', '') if price_elem else "None"
        
        link_elem = item.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        link = link_elem.get('href') if link_elem else (name_elem.find('a').get('href') if name_elem and name_elem.find('a') else "None")
        
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Link: {link}")
        print("---")
