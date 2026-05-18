# fetches store pages and hands them to the right parser.
# each retailer lays out its pages differently so they each get their
# own parser in the parsers/ folder.

import requests
from parsers import nike, footlocker, shopify

# which parser to use for each store
PARSERS = {
    "nike": nike.parse,
    "footlocker": footlocker.parse,
    "shopify": shopify.parse,
}


def fetch(url):
    headers = {"User-Agent": "InfoBots"}
    r = requests.get(url, headers=headers, timeout=10)
    # without this a 404/500 page gets handed to the parser as if it
    # were a real product page
    r.raise_for_status()
    return r.text


def scrape(target):
    parser_name = target["parser"]
    if parser_name not in PARSERS:
        raise ValueError("no parser called '{}' (store: {})".format(
            parser_name, target["store"]))
    text = fetch(target["url"])
    parse = PARSERS[parser_name]
    products = parse(text)
    # the parser doesn't know the store name so add it on here
    for p in products:
        p["store"] = target["store"]
    return products
