import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

search = "samsung galaxy s23"

# ------ Reliance Digital (deep parse) ------
print("=== Reliance Digital (deep) ===")
try:
    url = f"https://www.reliancedigital.in/search?q={search.replace(' ', '+')}:relevance"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Try various product card selectors
    for selector in ['div.product', 'div[class*="product"]', 'li[class*="product"]',
                     'div[class*="Product"]', 'div[class*="card"]', 'div[class*="Card"]',
                     'div[class*="item"]', 'div[class*="Item"]']:
        found = soup.select(selector)
        if found:
            print(f"  Selector '{selector}': {len(found)} items")
            if len(found) > 2:
                sample = found[0]
                print("  Sample text:", sample.text.strip()[:200])
                break

    # Try finding price spans with rupee
    price_spans = soup.find_all('span', string=re.compile(r'[\u20b9\d,]+'))
    print(f"  Price-like spans: {len(price_spans)}")
    for ps in price_spans[:5]:
        print("  =>", ps.text.strip()[:50])

    # Save HTML for inspection
    with open('reliance_digital.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print("  Saved to reliance_digital.html")
except Exception as e:
    print("Error:", e)

# ------ Paytm Mall (deep parse) ------
print("\n=== Paytm Mall (deep) ===")
try:
    url = f"https://paytmmall.com/shop/search?q={search.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')

    for selector in ['div[class*="product"]', 'div[class*="Product"]',
                     'div[class*="item"]', 'div[class*="card"]']:
        found = soup.select(selector)
        if found:
            print(f"  Selector '{selector}': {len(found)} items")

    # Check if it's React/JS rendered (empty shell)
    scripts = soup.find_all('script', src=False)
    print(f"  Inline scripts: {len(scripts)}")
    print("  Body text length:", len(soup.body.text.strip()) if soup.body else 0)
    print("  Preview:", soup.body.text.strip()[:200] if soup.body else "no body")
except Exception as e:
    print("Error:", e)

# ------ Vijay Sales (correct URL) ------
print("\n=== Vijay Sales ===")
try:
    url = f"https://www.vijaysales.com/search?q={search.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for selector in ['div[class*="product"]', 'div[class*="Product"]', 'div[class*="item"]']:
        found = soup.select(selector)
        if found and len(found) > 1:
            print(f"  Selector '{selector}': {len(found)} items")
    print("  Preview:", r.text[:400])
except Exception as e:
    print("Error:", e)
