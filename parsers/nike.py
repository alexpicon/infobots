# parser for the nike style page - a grid of product cards

from bs4 import BeautifulSoup


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.find_all("div", class_="product-card"):
        name = card.find("div", class_="product-card__title")
        price = card.find("div", class_="product-price")
        avail = card.find("div", class_="product-card__availability")
        if not (name and price and avail):
            # a card missing fields is usually an ad/placeholder - skip it
            # instead of crashing the whole run on a None.text
            print("  (skipping a malformed Nike card)")
            continue
        products.append({
            "url": card.get("data-pdp-url"),
            "name": name.text.strip(),
            "price": price.text.strip(),
            "in_stock": 1 if avail.text.strip().lower() == "available" else 0,
        })
    return products
