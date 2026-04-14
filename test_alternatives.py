import requests
from bs4 import BeautifulSoup
import json

# Test Flipkart via their internal search API (mobile/lite endpoint)
search = "iphone 13"

# Try Flipkart's organic search via different approach
urls_to_try = [
    f"https://www.flipkart.com/search?q={search.replace(' ', '+')}&otracker=search&otracker1=search",
    f"https://www.flipkart.com/search?q={search.replace(' ', '+')}",
]

mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Connection': 'keep-alive',
}

for url in urls_to_try:
    print(f"\nTrying: {url[:80]}")
    r = requests.get(url, headers=mobile_headers, timeout=15)
    print('Status:', r.status_code)
    if r.status_code == 200 and 'recaptcha' not in r.text.lower():
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('a', target='_blank')
        print('Items found:', len(items))
        if items:
            print("SUCCESS with mobile UA!")
            for item in items[:3]:
                img = item.find('img')
                if img and img.get('alt'):
                    print('Title:', img.get('alt')[:50])
            break
    else:
        if 'recaptcha' in r.text.lower():
            print('Got reCAPTCHA challenge')
        
# Try Bing Shopping scrape as alternative for Flipkart/Amazon data
print("\n\n--- Testing Bing Shopping (Free Alternative) ---")
bing_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-IN,en;q=0.9',
}
bing_url = f"https://www.bing.com/shop/search?q={search.replace(' ', '+')}&setlang=en-IN"
r_bing = requests.get(bing_url, headers=bing_headers, timeout=15)
print('Bing Shopping status:', r_bing.status_code)
soup_bing = BeautifulSoup(r_bing.text, 'html.parser')
products = soup_bing.find_all('li', class_=lambda x: x and 'br-item' in x)
print('Bing products found:', len(products))
