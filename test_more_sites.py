import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

search = "samsung galaxy s23"

# ------ Tata Cliq ------
print("=== Tata Cliq ===")
try:
    url = f"https://www.tatacliq.com/search/?searchCategory=all&text={search.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code, "| Len:", len(r.text))
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', class_=lambda x: x and 'ProductModule' in x)
    print("Items:", len(items))
    print("Preview:", r.text[:300])
except Exception as e:
    print("Error:", e)

# ------ Reliance Digital ------
print("\n=== Reliance Digital ===")
try:
    url = f"https://www.reliancedigital.in/search?q={search.replace(' ', '+')}:relevance"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code, "| Len:", len(r.text))
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', class_=lambda x: x and 'product' in (x or '').lower())
    print("Items:", len(items))
    print("Preview:", r.text[:300])
except Exception as e:
    print("Error:", e)

# ------ Vijay Sales ------
print("\n=== Vijay Sales ===")
try:
    url = f"https://www.vijaysales.com/search/{search.replace(' ', '-')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code, "| Len:", len(r.text))
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', class_=lambda x: x and 'product' in (x or '').lower())
    print("Items:", len(items))
    print("Preview:", r.text[:300])
except Exception as e:
    print("Error:", e)

# ------ Paytm Mall ------
print("\n=== Paytm Mall ===")
try:
    url = f"https://paytmmall.com/shop/search?q={search.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code, "| Len:", len(r.text))
    print("Preview:", r.text[:300])
except Exception as e:
    print("Error:", e)

# ------ Jiomart ------
print("\n=== Jiomart ===")
try:
    url = f"https://www.jiomart.com/search/{search.replace(' ', '%20')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    print("Status:", r.status_code, "| Len:", len(r.text))
    print("Preview:", r.text[:300])
except Exception as e:
    print("Error:", e)
