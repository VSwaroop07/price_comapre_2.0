import requests
from bs4 import BeautifulSoup

search = "iphone 13"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
}

# Test Meesho
print("--- Testing Meesho ---")
url_meesho = f'https://www.meesho.com/search?q={search.replace(" ", "%20")}'
try:
    r = requests.get(url_meesho, headers=HEADERS, timeout=15)
    print('Meesho status:', r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Meesho is React-rendered, check if we get any data
    if 'window.__INITIAL_STATE__' in r.text:
        print('Found initial state data')
    print('Response length:', len(r.text))
    print('Preview:', r.text[:300])
except Exception as e:
    print('Meesho error:', e)

# Test Snapdeal
print("\n--- Testing Snapdeal ---")
url_sd = f'https://www.snapdeal.com/search?keyword={search.replace(" ", "+")}'
try:
    r = requests.get(url_sd, headers=HEADERS, timeout=15)
    print('Snapdeal status:', r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', class_='product-tuple-description')
    print('Snapdeal items found:', len(items))
    if items:
        for item in items[:3]:
            name = item.find('p', class_='product-title')
            price = item.find('span', class_='lfloat product-price')
            print('Name:', name.text.strip()[:50] if name else 'None')
            print('Price:', price.text.strip()[:20] if price else 'None')
            print('---')
except Exception as e:
    print('Snapdeal error:', e)

# Test Croma
print("\n--- Testing Croma ---")
url_cr = f'https://www.croma.com/searchB?q={search.replace(" ", "+")}%3Arelevance&text={search.replace(" ", "+")}'
try:
    r = requests.get(url_cr, headers=HEADERS, timeout=15)
    print('Croma status:', r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('li', class_=lambda x: x and 'product' in x.lower())
    print('Croma items found:', len(items))
    print('Preview:', r.text[:500])
except Exception as e:
    print('Croma error:', e)
