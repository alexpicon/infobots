# parser for the foot locker style page - a plain product list

from bs4 import BeautifulSoup


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for li in soup.find_all("li", class_="product"):
        link = li.find("a", class_="ProductName")
        price = li.find("span", class_="ProductPrice").text.strip()
        stock = li.find("span", class_="ProductStock").text.strip().lower()
        products.append({
            "url": link.get("href"),
            "name": link.text.strip(),
            "price": price,
            "in_stock": 1 if stock == "in stock" else 0,
        })
    return products
