import cloudscraper
from bs4 import BeautifulSoup

search = "iphone 13"

print("--- Testing Flipkart with cloudscraper ---")
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

url_fk = f'https://www.flipkart.com/search?q={search.replace(" ", "+")}'
try:
    r = scraper.get(url_fk, timeout=30)
    print('Status:', r.status_code)
    if r.status_code == 200:
        if 'recaptcha' in r.text.lower():
            print('Got reCAPTCHA - cloudscraper did NOT bypass it')
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            items = soup.find_all('a', target='_blank', rel='noopener noreferrer')
            print(f'Items found: {len(items)}')
            count = 0
            for item in items:
                img = item.find('img')
                title = img.get('alt') if img else None
                if title and title.strip():
                    print(f'Title: {title[:50]}')
                    for d in item.find_all('div'):
                        t = d.text.strip()
                        if t.startswith('₹'):
                            print(f'Price: {t[:20]}')
                            break
                    print('---')
                    count += 1
                    if count >= 3:
                        break
    else:
        print('Response preview:', r.text[:500])
except Exception as e:
    print('Error:', e)
