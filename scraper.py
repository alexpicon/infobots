# gets product info off a store page
# only knows my mock store layout right now, can add real stores later

import requests
from bs4 import BeautifulSoup


def fetch(url):
    headers = {"User-Agent": "InfoBots"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.text


def parse_products(html, store):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for div in soup.find_all("div", class_="product"):
        name = div.find("span", class_="name").text.strip()
        price = div.find("span", class_="price").text.strip()
        stock = div.find("span", class_="stock").text.strip().lower()
        products.append({
            "url": div.get("data-url"),
            "name": name,
            "store": store,
            "price": price,
            "in_stock": 1 if stock == "in stock" else 0,
        })
    return products


def scrape(url, store):
    html = fetch(url)
    return parse_products(html, store)
