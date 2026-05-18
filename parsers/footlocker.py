# parser for the foot locker style page - a plain product list

from bs4 import BeautifulSoup


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for li in soup.find_all("li", class_="product"):
        link = li.find("a", class_="ProductName")
        price = li.find("span", class_="ProductPrice")
        stock = li.find("span", class_="ProductStock")
        if not (link and price and stock):
            # missing fields - skip it instead of crashing on a None.text
            print("  (skipping a malformed Foot Locker product)")
            continue
        products.append({
            "url": link.get("href"),
            "name": link.text.strip(),
            "price": price.text.strip(),
            "in_stock": 1 if stock.text.strip().lower() == "in stock" else 0,
        })
    return products
