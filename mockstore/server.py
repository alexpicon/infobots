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


if __name__ == "__main__":
    print("mock store running on http://127.0.0.1:5000")
    app.run(port=5000)
