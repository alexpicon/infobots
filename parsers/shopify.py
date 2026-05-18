# parser for shopify stores. shopify sites expose a /products.json endpoint
# so for these i don't scrape html at all, i just read the json.
# a lot of the smaller sneaker boutiques ran on shopify.

import json


def parse(text):
    data = json.loads(text)
    products = []
    for prod in data.get("products", []):
        variant = prod["variants"][0]
        products.append({
            "url": "/products/" + prod["handle"],
            "name": prod["title"],
            "price": "$" + variant["price"],
            "in_stock": 1 if variant["available"] else 0,
        })
    return products
