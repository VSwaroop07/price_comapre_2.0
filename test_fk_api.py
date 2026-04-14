import requests
from bs4 import BeautifulSoup
import urllib.parse

# Test ScrapingDog free API for Flipkart
# Sign up at https://scrapingdog.com - 1000 free API calls/month

# For now test if we can get Flipkart via their internal API endpoint
search = "iphone 13"

# Flipkart has an internal search API used by their mobile app
fk_api_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FKUA/website/41/website/Desktop',
}

# Try Flipkart's search suggestion API (public, no auth)
suggest_url = f"https://www.flipkart.com/api/4/page/fetch"
params = {
    'url': f'/search?q={urllib.parse.quote(search)}&sort=popularity',
    'type': 'PAGELOAD'
}

try:
    print("Testing Flipkart internal API...")
    r = requests.post(suggest_url, json=params, headers=fk_api_headers, timeout=20)
    print("Status:", r.status_code)
    if r.status_code == 200:
        print("SUCCESS! Got JSON response")
        data = r.json()
        print("Keys:", list(data.keys())[:5])
    else:
        print("Response:", r.text[:300])
except Exception as e:
    print("Error:", e)

# Also test with GET
print("\nTesting Flipkart GET API...")
try:
    r2 = requests.get(suggest_url, params=params, headers=fk_api_headers, timeout=20)
    print("Status:", r2.status_code)
    print("Response:", r2.text[:300])
except Exception as e:
    print("Error:", e)
