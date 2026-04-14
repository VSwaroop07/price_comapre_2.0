from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from bs4 import BeautifulSoup
import requests

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
                # Fallback: scan all spans
                for span in item.find_all('span'):
                    text = span.text.strip()
                    if '\u20b9' in text or (text.replace(',', '').isdigit() and len(text) > 2):
                        clean = text.replace('\u20b9', '').replace(',', '').strip()
                        if '.' in clean:
                            clean = clean.split('.')[0]
                        if clean.isdigit():
                            # Deduplicate doubled text Amazon sometimes creates
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
# Scraper: Snapdeal India (replaces Flipkart which enforces reCAPTCHA)
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
            # e.g. "Rs. 1,499" → "1499"
            price_val = price_text.replace('Rs.', '').replace(',', '').strip()
            if not price_val or not price_val.replace('.', '').isdigit():
                continue
            # Drop decimals
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
# View
# ---------------------------------------------------------------------------
def index(request):
    content = {}
    content['title'] = 'Welcome to price compare'

    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        if search:
            am_list = scrape_amazon(search)
            sd_list = scrape_snapdeal(search)
            sc_list = scrape_shopclues(search)

            total_list = am_list + sd_list + sc_list

            def sort_key(d):
                try:
                    return int(d['price'])
                except (ValueError, TypeError):
                    return 999999

            content['total_list'] = sorted(total_list, key=sort_key)

    return render(request, 'index.html', content)