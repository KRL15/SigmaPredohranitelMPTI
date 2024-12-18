import re
import requests
from bs4 import BeautifulSoup

def pars_subjects():
    names_and_prices = {}
    url = f'https://avtorup.ru/catalog/predokhraniteli-derzhateli-predokhranitelejj/page/1'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    data = soup.find_all('div', 'item')
    for item in data:
        name = item.find('div', 'brief text')
        price = item.find('div', 'price')
        if name and price:
            names_and_prices[name.text.strip()] = price.text.strip()
    return names_and_prices

def extract_types(name):
    types = re.findall(r'\d+[A|a]', name)
    return types

def parse_fuse_data(data):
    fuses = []
    for name, price_str in data.items():
        price_match = re.search(r'Цена: (\d+\.\d+) руб.', price_str)
        if price_match:
            price = float(price_match.group(1))
            fuse = {
                'name': name,
                'price': price,
                'types': extract_types(name),
                'ratings': [],
                'comments': []
            }
            fuses.append(fuse)
    return fuses
