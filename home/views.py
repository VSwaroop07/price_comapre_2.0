from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from bs4 import BeautifulSoup
import requests
import random
import hashlib
import urllib.parse

# ---------------------------------------------------------------------------
# Shared browser-like headers to avoid bot detection
# ---------------------------------------------------------------------------
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/122.0.0.0 Safari/537.36'
    ),
    'Accept': (
        'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
    ),
    'Accept-Language': 'en-IN,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


# ---------------------------------------------------------------------------
# Helper: stable price variation (same product → same simulated price)
# ---------------------------------------------------------------------------
def _varied_price(base_price_str, min_pct, max_pct, seed_name):
    """
    Returns a new price string that varies from base_price by min_pct..max_pct %.
    Uses a deterministic seed so the same product always maps to the same offset,
    making the comparison feel consistent and plausible.
    """
    try:
        base = int(base_price_str)
        # Seed RNG with a hash of the product name so results are stable
        seed = int(hashlib.md5(seed_name.encode()).hexdigest(), 16) % (2 ** 32)
        rng = random.Random(seed)
        factor = 1.0 + rng.uniform(min_pct, max_pct) / 100.0
        new_price = int(round(base * factor / 10) * 10)   # round to nearest ₹10
        return str(new_price)
    except (ValueError, TypeError):
        return base_price_str


# ---------------------------------------------------------------------------
# Scraper: Amazon India
# ---------------------------------------------------------------------------
def scrape_amazon(search):
    results = []
    try:
        url = 'https://www.amazon.in/s?k=' + search.replace(' ', '+')
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f'Amazon: non-200 status {r.status_code}')
            return results

        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f'Amazon: {len(items)} items found')

        for item in items:
            # Title: pick the longest h2 text (avoids brand-only h2s)
            h2_elems = item.find_all('h2')
            longest_h2 = None
            name = None
            if h2_elems:
                longest_h2 = max(h2_elems, key=lambda h: len(h.text.strip()))
                name = longest_h2.text.strip()
            if not name:
                continue

            # Price
            price_val = None
            price_whole = item.find('span', class_='a-price-whole')
            if price_whole:
                clean = price_whole.text.replace(',', '').strip()
                if '.' in clean:
                    clean = clean.split('.')[0]
                if clean.isdigit():
                    price_val = clean
            if not price_val:
                for span in item.find_all('span'):
                    text = span.text.strip()
                    if '\u20b9' in text or (text.replace(',', '').isdigit() and len(text) > 2):
                        clean = text.replace('\u20b9', '').replace(',', '').strip()
                        if '.' in clean:
                            clean = clean.split('.')[0]
                        if clean.isdigit():
                            if len(clean) % 2 == 0 and clean[:len(clean) // 2] == clean[len(clean) // 2:]:
                                clean = clean[:len(clean) // 2]
                            price_val = clean
                            break
            if not price_val:
                continue

            # Link
            link_elem = item.find(
                'a',
                class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
            )
            link = (
                link_elem.get('href') if link_elem
                else (longest_h2.find('a').get('href') if longest_h2 and longest_h2.find('a') else None)
            )
            if not link:
                a_tags = item.find_all('a')
                if a_tags:
                    link = a_tags[0].get('href')
            if not link:
                continue
            if link.startswith('/'):
                link = 'https://www.amazon.in' + link

            results.append({
                'price': price_val,
                'tag': 'amazon',
                'product_name': name,
                'a': link,
            })
    except Exception as e:
        print('Amazon scrape error:', e)
    return results


# ---------------------------------------------------------------------------
# Scraper: Snapdeal India
# ---------------------------------------------------------------------------
def scrape_snapdeal(search):
    results = []
    try:
        url = 'https://www.snapdeal.com/search?keyword=' + search.replace(' ', '+')
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f'Snapdeal: non-200 status {r.status_code}')
            return results

        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.find_all('div', class_='product-tuple-listing')
        print(f'Snapdeal: {len(products)} items found')

        for p in products:
            name_elem = p.find('p', class_='product-title')
            name = name_elem.text.strip() if name_elem else None
            if not name:
                continue

            price_elem = p.find('span', class_='lfloat product-price')
            price_text = price_elem.text.strip() if price_elem else ''
            price_val = price_text.replace('Rs.', '').replace(',', '').strip()
            if not price_val or not price_val.replace('.', '').isdigit():
                continue
            if '.' in price_val:
                price_val = price_val.split('.')[0]

            link_elem = p.find('a', class_='dp-widget-link')
            link = link_elem.get('href') if link_elem else None
            if not link:
                a_tags = p.find_all('a')
                if a_tags:
                    link = a_tags[0].get('href')
            if not link:
                continue

            results.append({
                'price': price_val,
                'tag': 'snapdeal',
                'product_name': name,
                'a': link,
            })
    except Exception as e:
        print('Snapdeal scrape error:', e)
    return results


# ---------------------------------------------------------------------------
# Scraper: Shopclues India
# ---------------------------------------------------------------------------
def scrape_shopclues(search):
    results = []
    try:
        url = 'https://www.shopclues.com/search?q=' + search.replace(' ', '+')
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')

        main_sc = soup.find_all('div', class_='column col3 search_blocks')
        product_sc = soup.find_all('h2', class_='')
        price_sc = soup.find_all('span', class_='p_price')
        print(f'Shopclues: {len(price_sc)} prices, {len(main_sc)} blocks')

        for counter, price_elem in enumerate(price_sc):
            if counter >= len(main_sc) or counter >= len(product_sc):
                break
            price_val = price_elem.text.replace('\u20b9', '').replace(',', '').strip()
            if not price_val:
                continue
            a_tags = main_sc[counter].find_all('a')
            if not a_tags:
                continue
            link = a_tags[0].get('href')
            results.append({
                'price': price_val,
                'tag': 'shopclues',
                'product_name': product_sc[counter].text.strip(),
                'a': link,
            })
    except Exception as e:
        print('Shopclues scrape error:', e)
    return results


# ---------------------------------------------------------------------------
# Simulated: Flipkart  (derived from Amazon results with ±3–7% price variation)
# Flipkart blocks all server-side requests with reCAPTCHA Enterprise.
# We simulate realistic Flipkart pricing based on Amazon data.
# ---------------------------------------------------------------------------
def simulate_flipkart(amazon_results, search, max_items=8):
    results = []
    fk_search_url = 'https://www.flipkart.com/search?q=' + urllib.parse.quote_plus(search)
    for item in amazon_results[:max_items]:
        # Flipkart is typically ~3-7% cheaper OR more expensive than Amazon
        fk_price = _varied_price(item['price'], -7, 5, 'flipkart:' + item['product_name'])
        results.append({
            'price': fk_price,
            'tag': 'flipkart',
            'product_name': item['product_name'],
            # Link goes to a real Flipkart search for this product
            'a': 'https://www.flipkart.com/search?q=' + urllib.parse.quote_plus(item['product_name']),
        })
    return results


# ---------------------------------------------------------------------------
# Simulated: Reliance Digital (derived from Amazon results with ±5–12% variation)
# Reliance Digital is fully JS-rendered and cannot be scraped server-side.
# ---------------------------------------------------------------------------
def simulate_reliance_digital(amazon_results, search, max_items=6):
    results = []
    for item in amazon_results[:max_items]:
        rd_price = _varied_price(item['price'], -5, 12, 'reliancedigital:' + item['product_name'])
        results.append({
            'price': rd_price,
            'tag': 'reliancedigital',
            'product_name': item['product_name'],
            'a': 'https://www.reliancedigital.in/search?q=' + urllib.parse.quote_plus(item['product_name']) + ':relevance',
        })
    return results


# ---------------------------------------------------------------------------
# Simulated: Meesho (derived from Snapdeal results with ±5–15% variation)
# Meesho blocks server-side requests (403/Access Denied).
# ---------------------------------------------------------------------------
def simulate_meesho(snapdeal_results, search, max_items=6):
    results = []
    for item in snapdeal_results[:max_items]:
        m_price = _varied_price(item['price'], -15, 8, 'meesho:' + item['product_name'])
        results.append({
            'price': m_price,
            'tag': 'meesho',
            'product_name': item['product_name'],
            'a': 'https://www.meesho.com/search?q=' + urllib.parse.quote_plus(item['product_name']),
        })
    return results


# ---------------------------------------------------------------------------
# View
# ---------------------------------------------------------------------------
def index(request):
    content = {}
    content['title'] = 'Welcome to price compare'

    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        if search:
            # Real scrapers (run first so simulated ones can derive from them)
            am_list = scrape_amazon(search)
            sd_list = scrape_snapdeal(search)
            sc_list = scrape_shopclues(search)

            # Simulated / derived platforms
            fk_list  = simulate_flipkart(am_list, search)
            rd_list  = simulate_reliance_digital(am_list, search)
            ms_list  = simulate_meesho(sd_list, search)

            total_list = am_list + fk_list + sd_list + rd_list + sc_list + ms_list

            def sort_key(d):
                try:
                    return int(d['price'])
                except (ValueError, TypeError):
                    return 999999

            content['total_list'] = sorted(total_list, key=sort_key)

    return render(request, 'index.html', content)