import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'c:\Users\vyawa\OneDrive\Desktop\price_comapre_2.0')

from home.views import (scrape_amazon, scrape_snapdeal, scrape_shopclues,
                        simulate_flipkart, simulate_reliance_digital, simulate_meesho)

search = 'iphone 14'
am = scrape_amazon(search)
sd = scrape_snapdeal(search)
sc = scrape_shopclues(search)
fk = simulate_flipkart(am, search)
rd = simulate_reliance_digital(am, search)
ms = simulate_meesho(sd, search)

print()
print('=== RESULTS SUMMARY ===')
print(f'Amazon:           {len(am)} real results')
print(f'Flipkart:         {len(fk)} simulated results')
print(f'Snapdeal:         {len(sd)} real results')
print(f'Reliance Digital: {len(rd)} simulated results')
print(f'Shopclues:        {len(sc)} real results')
print(f'Meesho:           {len(ms)} simulated results')
print(f'GRAND TOTAL:      {len(am)+len(fk)+len(sd)+len(rd)+len(sc)+len(ms)} products')

if am:
    ref = am[0]
    pname = ref['product_name'][:45]
    print(f'\nSample prices for: {pname}')
    print(f'  Amazon price:           {ref["price"]}')
    fk_match = next((x for x in fk if x['product_name'] == ref['product_name']), None)
    rd_match = next((x for x in rd if x['product_name'] == ref['product_name']), None)
    if fk_match: print(f'  Flipkart price:         {fk_match["price"]}')
    if rd_match: print(f'  Reliance Digital price: {rd_match["price"]}')
