import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

print("--- Testing Amazon ---")
url_am = 'https://www.amazon.in/s?k=iphone+13'
r_am = requests.get(url_am, headers=HEADERS, timeout=20)
print('Amazon status:', r_am.status_code)
soup_am = BeautifulSoup(r_am.text, 'html.parser')
items_am = soup_am.find_all('div', {'data-component-type': 's-search-result'})
print('Amazon items found:', len(items_am))
if items_am:
    item = items_am[0]
    h2 = item.find('h2')
    price = item.find('span', class_='a-price-whole')
    print('Name:', h2.text.strip() if h2 else 'None')
    print('Price:', price.text.strip() if price else 'None')

print()
print("--- Testing Flipkart ---")
fk_headers = {**HEADERS, 'Referer': 'https://www.flipkart.com/'}
url_fk = 'https://www.flipkart.com/search?q=iphone+13'
r_fk = requests.get(url_fk, headers=fk_headers, timeout=20)
print('Flipkart status:', r_fk.status_code)
soup_fk = BeautifulSoup(r_fk.text, 'html.parser')

items_fk = soup_fk.find_all('a', target='_blank', rel='noopener noreferrer')
print('FK items (a noopener):', len(items_fk))

for item in items_fk[:3]:
    img = item.find('img')
    title = img.get('alt') if img else None
    if not title or title.strip() == "":
        continue
    print('Title:', title)
    divs = item.find_all('div')
    for d in divs:
        text = d.text.strip()
        if text.startswith('₹'):
            print('Price:', text[:30])
            break
    print('---')
