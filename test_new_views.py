import sys
sys.path.insert(0, r'c:\Users\vyawa\OneDrive\Desktop\price_comapre_2.0')

# Import and test the new scraper functions directly
from home.views import scrape_amazon, scrape_snapdeal, scrape_shopclues

search = "samsung galaxy s23"

print("=" * 50)
print("TEST: Amazon")
print("=" * 50)
am = scrape_amazon(search)
for p in am[:3]:
    print(f"  [{p['tag']}] {p['product_name'][:50]} — ₹{p['price']}")
print(f"  Total: {len(am)} results\n")

print("=" * 50)
print("TEST: Snapdeal")
print("=" * 50)
sd = scrape_snapdeal(search)
for p in sd[:3]:
    print(f"  [{p['tag']}] {p['product_name'][:50]} — ₹{p['price']}")
print(f"  Total: {len(sd)} results\n")

print("=" * 50)
print("TEST: Shopclues")
print("=" * 50)
sc = scrape_shopclues(search)
for p in sc[:3]:
    print(f"  [{p['tag']}] {p['product_name'][:50]} — ₹{p['price']}")
print(f"  Total: {len(sc)} results\n")

total = am + sd + sc
print(f"GRAND TOTAL: {len(total)} products from all sources")
