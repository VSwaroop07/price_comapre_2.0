import re

with open('reliance_digital.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print('Total chars:', len(content))
print('Title:', re.search(r'<title>(.*?)</title>', content, re.IGNORECASE).group(1) if re.search(r'<title>(.*?)</title>', content, re.IGNORECASE) else 'No title')

# Look for product data
if 'productName' in content:
    print('Has productName!')
if 'sellingPrice' in content:
    print('Has sellingPrice!')
if 'originalPrice' in content:
    print('Has originalPrice!')
if 'displayName' in content:
    print('Has displayName!')

# Find price mentions
prices = re.findall(r'"price":(\d+)', content)
print('Price values found:', prices[:10])

names = re.findall(r'"displayName":"([^"]{5,60})"', content)
print('displayName values:', names[:5])

names2 = re.findall(r'"productName":"([^"]{5,60})"', content)
print('productName values:', names2[:5])

names3 = re.findall(r'"name":"([^"]{5,60})"', content)
print('name values:', names3[:8])
