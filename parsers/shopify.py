# parser for shopify stores. shopify sites expose a /products.json endpoint
# so for these i don't scrape html at all, i just read the json.
# a lot of the smaller sneaker boutiques ran on shopify.

import json


def parse(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # the endpoint returned something that wasn't json (error page etc)
        print("  (Shopify feed wasn't valid JSON, skipping store)")
        return []
    products = []
    for prod in data.get("products", []):
        variants = prod.get("variants", [])
        if not variants:
            # a product with no variants has no price/stock to read
            continue
        variant = variants[0]
        products.append({
            "url": "/products/" + prod.get("handle", ""),
            "name": prod.get("title", ""),
            "price": "$" + variant.get("price", "0"),
            "in_stock": 1 if variant.get("available") else 0,
        })
    return products
