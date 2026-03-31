from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from bs4 import BeautifulSoup
import requests
import urllib.parse

API_KEY = "0d3c058d03367f0dd63047cb4d8454ff"

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'in'}
    return "https://api.scraperapi.com/?" + urllib.parse.urlencode(payload)


# Create your views here.
def index(request):
    content = {}
    content['title'] = 'Welcome to price compare'
    if request.method == 'POST':
        search = request.POST['search']
        # Flipkart search
        url_link_fk = "https://www.flipkart.com/search?q=" + search.replace(' ', '+')
        fk_list = []
        try:
            # Flipkart requires premium proxies to bypass bot protection reliably
            payload_fk = {'api_key': API_KEY, 'url': url_link_fk, 'country_code': 'in', 'premium': 'true'}
            scraper_url_fk = "https://api.scraperapi.com/?" + urllib.parse.urlencode(payload_fk)
            
            response_fk = requests.get(scraper_url_fk)
            if response_fk.status_code == 200:
                soup_fk = BeautifulSoup(response_fk.text, 'html.parser')
                main_fk = soup_fk.find_all('a', target='_blank', rel='noopener noreferrer')
                
                print(f"FK Scraper status: {response_fk.status_code}, Items found: {len(main_fk)}")
                
                for item in main_fk:
                    href = item.get('href') if item.name == 'a' else item.find('a').get('href') if item.find('a') else "None"
                    
                    img = item.find('img')
                    title = img.get('alt') if img else None
                    if not title or title.strip() == "": continue
                    
                    divs = item.find_all('div')
                    price_val = None
                    for d in divs:
                         text = d.text.strip()
                         if text.startswith('₹') and len(text) > 1 and len(text) < 15 and ',' in text:
                             price_val = text.replace('₹', '').replace(',', '')
                             break
                    
                    if title and price_val and href and href != "None":
                        url_ = "https://www.flipkart.com" + href if href.startswith('/') else href
                        fk_dict = {'price': price_val, 'tag': 'flipkart', 'product_name': title, 'a': url_}
                        fk_list.append(fk_dict)
        except Exception as e:
            print("Flipkart scrape error:", e)

        # Amazon
        url_link_am = "https://www.amazon.in/s?k=" + search.replace(' ', '+')
        am_list = []
        try:
            response_am = requests.get(get_scraperapi_url(url_link_am))
            if response_am.status_code == 200:
                soup_am = BeautifulSoup(response_am.text, 'html.parser')
                items = soup_am.find_all('div', {'data-component-type': 's-search-result'})
                print(f"AM Scraper status: {response_am.status_code}, Items found: {len(items)}")
                for item in items:
                    h2_elems = item.find_all('h2')
                    name = None
                    longest_h2 = None
                    if h2_elems:
                        # Amazon now puts the brand in the first h2 and the title in the second
                        # The actual title is always the longest one
                        longest_h2 = max(h2_elems, key=lambda h: len(h.text.strip()))
                        name = longest_h2.text.strip()
                    
                    price_val = None
                    # Amazon prices usually have the Rupee symbol
                    # We will find the first span with a-price-whole or fallback to generic
                    price_whole_span = item.find('span', class_='a-price-whole')
                    if price_whole_span:
                        clean = price_whole_span.text.replace('₹', '').replace(',', '').strip()
                        if '.' in clean: clean = clean.split('.')[0]
                        if clean.isdigit(): price_val = clean
                    else:
                        for span in item.find_all('span'):
                            text = span.text.strip()
                            if '₹' in text or (text.replace(',', '').isdigit() and len(text) > 3):
                                 clean = text.replace('₹', '').replace(',', '').strip()
                                 if '.' in clean: clean = clean.split('.')[0]
                                 if clean.isdigit():
                                     # Sometimes Amazon nests spans, causing double text like "9999999999"
                                     # if length is even and halves match, it's doubled
                                     if len(clean) % 2 == 0 and clean[:len(clean)//2] == clean[len(clean)//2:]:
                                         clean = clean[:len(clean)//2]
                                     price_val = clean
                                     break
                    
                    link_elem = item.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
                    link = link_elem.get('href') if link_elem else (longest_h2.find('a').get('href') if longest_h2 and longest_h2.find('a') else None)
                    if not link:
                         # just grab any link
                         a_tags = item.find_all('a')
                         if a_tags: link = a_tags[0].get('href')
                    
                    if name and price_val and link:
                        url_ = "https://www.amazon.in" + link if link.startswith('/') else link
                        am_dict = {'price': price_val, 'tag': 'amazon', 'product_name': name, 'a': url_}
                        am_list.append(am_dict)
        except Exception as e:
            print("Amazon scrape error:", e)

        # Shopclues
        url_link_sc = "https://www.shopclues.com/search?q=" + search.replace(' ', '+')
        response_sc = requests.get(url_link_sc)
        soup_sc = BeautifulSoup(response_sc.text, 'html.parser')
        main_sc = soup_sc.find_all('div', class_='column col3 search_blocks')
        product_sc = soup_sc.find_all('h2', class_='')
        # print(product_sc)
        price_sc = soup_sc.find_all('span', class_='p_price')
        print(len(price_sc))
        print(len(main_sc))
        sc_list = []
        counter = 0
        for i in price_sc:
            price = i.text.replace('₹','')
            price = price.replace(',','')
            a_class = main_sc[counter].find_all('a')
            url_ = a_class[0].get('href')
            sc_dict = {'price':price, 'tag':'shopclues', 'product_name':product_sc[counter].text, 'a':url_}
            sc_list.append(sc_dict)
            counter += 1
        # print(sc_list)
        # content['fk_list'] = sorted(sc_list, key=lambda d: d['price'])

        total_list = fk_list + sc_list + am_list
        content['total_list'] = sorted(total_list, key=lambda d: int(d['price']) if str(d['price']).isdigit() else 999999)
    return render(request, 'index.html', content)