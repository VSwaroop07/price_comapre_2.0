import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

search = "samsung galaxy s23"

# Croma - try different endpoints
for url in [
    f"https://www.croma.com/searchB?q={search.replace(' ', '+')}%3Arelevance",
    f"https://www.croma.com/search/?q={search.replace(' ', '+')}",
    f"https://www.croma.com/catalogsearch/result/?q={search.replace(' ', '+')}",
]:
    print(f"Trying: {url[:70]}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        print(f"  Status: {r.status_code} | Len: {len(r.text)}")
        if r.status_code == 200 and 'Access Denied' not in r.text:
            soup = BeautifulSoup(r.text, 'html.parser')
            # look for product blocks
            for sel in ['div[class*="product-item"]', 'li[class*="product"]',
                        'div[class*="cp-product"]', 'div[class*="plp-card"]',
                        'div[class*="product-list"]']:
                found = soup.select(sel)
                if found:
                    print(f"  Found {len(found)} via '{sel}'")
                    print("  Sample:", found[0].text.strip()[:100])
                    break
            # check for JSON data
            for key in ['sellingPrice', 'finalPrice', 'mrPrice', 'productName']:
                if key in r.text:
                    print(f"  Has JSON key: {key}")
            prices = re.findall(r'"mrpPrice":(\d+)', r.text)
            print(f"  mrpPrice values: {prices[:5]}")
            names = re.findall(r'"name":"([^"]{5,60})"', r.text)
            print(f"  name values: {names[:3]}")
    except Exception as e:
        print(f"  Error: {e}")
    print()
