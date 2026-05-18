# fake store to test the bot against
# i made this because real sites block bots and its against their rules
# the products live in memory so they reset when you restart the server

from flask import Flask

app = Flask(__name__)

STORE = [
    {"slug": "yeezy-350-zebra", "name": "Yeezy Boost 350 V2 Zebra", "price": "$220", "stock": True},
    {"slug": "jordan-1-bred-toe", "name": "Air Jordan 1 Bred Toe", "price": "$160", "stock": True},
    {"slug": "dunk-low-panda", "name": "Nike Dunk Low Panda", "price": "$110", "stock": False},
    {"slug": "new-balance-550", "name": "New Balance 550 White Green", "price": "$120", "stock": True},
    {"slug": "yeezy-700-wave", "name": "Yeezy Boost 700 Wave Runner", "price": "$300", "stock": False},
]


def product_html(p):
    stock = "in stock" if p["stock"] else "sold out"
    return '''  <div class="product" data-url="/product/{slug}">
    <span class="name">{name}</span>
    <span class="price">{price}</span>
    <span class="stock">{stock}</span>
  </div>'''.format(slug=p["slug"], name=p["name"], price=p["price"], stock=stock)


@app.route("/")
def storefront():
    rows = "\n".join(product_html(p) for p in STORE)
    return "<html>\n<body>\n<h1>Demo Sneaker Store</h1>\n" + rows + "\n</body>\n</html>"


# little routes so i can change the store while the bot is running
# (restock stuff, change prices) without restarting the server

def find_product(slug):
    for p in STORE:
        if p["slug"] == slug:
            return p
    return None


@app.route("/admin/restock/<slug>")
def admin_restock(slug):
    p = find_product(slug)
    if p is None:
        return "no product called " + slug
    p["stock"] = True
    return slug + " is back in stock"


@app.route("/admin/soldout/<slug>")
def admin_soldout(slug):
    p = find_product(slug)
    if p is None:
        return "no product called " + slug
    p["stock"] = False
    return slug + " is now sold out"


@app.route("/admin/price/<slug>/<int:price>")
def admin_price(slug, price):
    p = find_product(slug)
    if p is None:
        return "no product called " + slug
    p["price"] = "$" + str(price)
    return slug + " price is now $" + str(price)


if __name__ == "__main__":
    print("mock store running on http://127.0.0.1:5000")
    app.run(port=5000)
