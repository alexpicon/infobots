# fetches store pages and hands them to the right parser.
# each retailer lays out its pages differently so they each get their
# own parser in the parsers/ folder.

import requests
from parsers import nike, footlocker

# which parser to use for each store
PARSERS = {
    "nike": nike.parse,
    "footlocker": footlocker.parse,
}


def fetch(url):
    headers = {"User-Agent": "InfoBots"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.text


def scrape(target):
    text = fetch(target["url"])
    parse = PARSERS[target["parser"]]
    products = parse(text)
    # the parser doesn't know the store name so add it on here
    for p in products:
        p["store"] = target["store"]
    return products
