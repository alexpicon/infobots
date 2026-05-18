# parser for the nike style page - a grid of product cards

from bs4 import BeautifulSoup


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.find_all("div", class_="product-card"):
        name = card.find("div", class_="product-card__title").text.strip()
        price = card.find("div", class_="product-price").text.strip()
        avail = card.find("div", class_="product-card__availability").text.strip().lower()
        products.append({
            "url": card.get("data-pdp-url"),
            "name": name,
            "price": price,
            "in_stock": 1 if avail == "available" else 0,
        })
    return products
