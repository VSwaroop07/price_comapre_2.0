import requests
from bs4 import BeautifulSoup

search = "iphone 13"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
}

# Full Snapdeal test to get name, price, url, and image
print("--- Full Snapdeal Test ---")
url_sd = f'https://www.snapdeal.com/search?keyword={search.replace(" ", "+")}'
r = requests.get(url_sd, headers=HEADERS, timeout=15)
print('Status:', r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')

# Find product cards
products = soup.find_all('div', class_='product-tuple-listing')
print('Products found:', len(products))

for p in products[:5]:
    # Name
    name_elem = p.find('p', class_='product-title')
    name = name_elem.text.strip() if name_elem else None
    
    # Price
    price_elem = p.find('span', class_='lfloat product-price')
    price_text = price_elem.text.strip() if price_elem else None
    price = price_text.replace('Rs. ', '').replace(',', '').strip() if price_text else None
    
    # URL
    link_elem = p.find('a', class_='dp-widget-link')
    url = link_elem.get('href') if link_elem else None
    
    # Image
    img_elem = p.find('img', class_='product-image')
    img = img_elem.get('src') if img_elem else None
    
    print(f'Name: {name[:50] if name else None}')
    print(f'Price: {price}')
    print(f'URL: {url[:60] if url else None}')
    print(f'Img: {img[:60] if img else None}')
    print('---')

# Full Amazon test to get name, price, url with link
print("\n--- Full Amazon Test ---")
url_am = f'https://www.amazon.in/s?k={search.replace(" ", "+")}'
r_am = requests.get(url_am, headers=HEADERS, timeout=20)
print('Status:', r_am.status_code)
soup_am = BeautifulSoup(r_am.text, 'html.parser')
items_am = soup_am.find_all('div', {'data-component-type': 's-search-result'})
print('Items found:', len(items_am))

for item in items_am[:3]:
    h2_elems = item.find_all('h2')
    name = None
    longest_h2 = None
    if h2_elems:
        longest_h2 = max(h2_elems, key=lambda h: len(h.text.strip()))
        name = longest_h2.text.strip()
    
    price_whole = item.find('span', class_='a-price-whole')
    price = None
    if price_whole:
        clean = price_whole.text.replace(',', '').strip()
        if '.' in clean:
            clean = clean.split('.')[0]
        price = clean if clean.isdigit() else None

    link_elem = item.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    link = link_elem.get('href') if link_elem else (longest_h2.find('a').get('href') if longest_h2 and longest_h2.find('a') else None)
    if link and not link.startswith('http'):
        link = 'https://www.amazon.in' + link

    print(f'Name: {name[:50] if name else None}')
    print(f'Price: {price}')
    print(f'URL: {link[:60] if link else None}')
    print('---')
