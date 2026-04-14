import requests
from bs4 import BeautifulSoup

# Try Flipkart with a session to get cookies first
session = requests.Session()

headers_home = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Connection': 'keep-alive',
}

# First visit homepage to get session cookies
print("Visiting Flipkart homepage...")
r_home = session.get('https://www.flipkart.com/', headers=headers_home, timeout=15)
print('Homepage status:', r_home.status_code)
print('Cookies:', dict(session.cookies))

# Now search
search_headers = {**headers_home, 'Referer': 'https://www.flipkart.com/'}
url_fk = 'https://www.flipkart.com/search?q=iphone+13'
r_fk = session.get(url_fk, headers=search_headers, timeout=20)
print('Search status:', r_fk.status_code)
soup = BeautifulSoup(r_fk.text, 'html.parser')

items = soup.find_all('a', target='_blank', rel='noopener noreferrer')
print('FK items:', len(items))
if items:
    for item in items[:3]:
        img = item.find('img')
        title = img.get('alt') if img else None
        if title and title.strip():
            print('Title:', title)
            for d in item.find_all('div'):
                t = d.text.strip()
                if t.startswith('₹'):
                    print('Price:', t[:20])
                    break
            print('---')
else:
    print("No items. Checking if captcha/login page...")
    print("Body preview:", r_fk.text[:1000])
