# fake stores to test the bot against
# i made this because real sites block bots and its against their rules.
# theres 3 "stores" here and each one renders its page differently, so the
# bot needs a different parser for each one - same as the real retailers did.

from flask import Flask, jsonify

app = Flask(__name__)

# the products are all stored the same way internally. each store route
# renders them in that retailers layout. resets when you restart the server.
STORES = {
    "nike": [
        {"id": "air-max-90-infrared", "name": "Nike Air Max 90 Infrared", "price": 130, "stock": True},
        {"id": "air-force-1-low", "name": "Nike Air Force 1 Low White", "price": 110, "stock": True},
        {"id": "dunk-low-panda", "name": "Nike Dunk Low Panda", "price": 115, "stock": False},
        {"id": "jordan-1-chicago", "name": "Air Jordan 1 High Chicago", "price": 180, "stock": False},
    ],
    "footlocker": [
        {"id": "nb-550-white-green", "name": "New Balance 550 White Green", "price": 120, "stock": True},
        {"id": "jordan-4-black-cat", "name": "Jordan 4 Retro Black Cat", "price": 210, "stock": False},
        {"id": "samba-og", "name": "adidas Samba OG", "price": 100, "stock": True},
    ],
    "solefly": [
        {"id": "yeezy-350-zebra", "name": "Yeezy Boost 350 V2 Zebra", "price": 220, "stock": True},
        {"id": "travis-jordan-1-low", "name": "Travis Scott Air Jordan 1 Low", "price": 1500, "stock": False},
        {"id": "dunk-chunky-dunky", "name": "Nike Dunk Low Chunky Dunky", "price": 850, "stock": True},
    ],
}


@app.route("/")
def index():
    return """<html><body>
<h1>Mock Stores</h1>
<p>fake stores for testing infobots:</p>
<ul>
  <li><a href="/nike">/nike</a> - nike style product grid</li>
  <li><a href="/footlocker">/footlocker</a> - foot locker style list</li>
  <li><a href="/solefly/products.json">/solefly/products.json</a> - shopify style json</li>
</ul>
</body></html>"""


# --- Nike: a grid of product cards ---

@app.route("/nike")
def nike_page():
    cards = ""
    for p in STORES["nike"]:
        avail = "Available" if p["stock"] else "Sold Out"
        cards += '''
  <div class="product-card" data-pdp-url="/t/{id}">
    <div class="product-card__title">{name}</div>
    <div class="product-price">${price}</div>
    <div class="product-card__availability">{avail}</div>
  </div>'''.format(id=p["id"], name=p["name"], price=p["price"], avail=avail)
    return '<html><body>\n<div class="product-grid">' + cards + "\n</div>\n</body></html>"


# --- admin routes so i can change the stores while the bot is running ---

def find_product(store, pid):
    for p in STORES.get(store, []):
        if p["id"] == pid:
            return p
    return None


@app.route("/admin/<store>/restock/<pid>")
def admin_restock(store, pid):
    p = find_product(store, pid)
    if p is None:
        return "no product " + pid + " in " + store
    p["stock"] = True
    return pid + " is back in stock at " + store


@app.route("/admin/<store>/soldout/<pid>")
def admin_soldout(store, pid):
    p = find_product(store, pid)
    if p is None:
        return "no product " + pid + " in " + store
    p["stock"] = False
    return pid + " is sold out at " + store


@app.route("/admin/<store>/price/<pid>/<int:price>")
def admin_price(store, pid, price):
    p = find_product(store, pid)
    if p is None:
        return "no product " + pid + " in " + store
    p["price"] = price
    return pid + " price at " + store + " is now $" + str(price)


if __name__ == "__main__":
    print("mock store running on http://127.0.0.1:5000")
    app.run(port=5000)
