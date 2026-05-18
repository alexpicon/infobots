# compares whats on the store right now vs what we saw last time
# returns a list of alerts for the bot to send out

import datetime
import database


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def price_to_number(price):
    # prices come in as text like "$220" so comparing them as strings was wrong
    # ("$90" < "$120" is False because it compares letter by letter)
    # this strips it down to an actual number
    p = price.replace("$", "").replace(",", "").strip()
    try:
        return float(p)
    except ValueError:
        return 0.0


def add_alert(alerts, url, atype, message):
    # i was writing these same two lines every time so i pulled it out
    alerts.append({"url": url, "type": atype, "message": message})
    database.log_alert(url, atype, message)


def check(products, keywords):
    alerts = []
    for p in products:
        old = database.get_product(p["url"])
        if old is None:
            # never seen this product before
            msg = "New product: {} - {}".format(p["name"], p["price"])
            add_alert(alerts, p["url"], "new", msg)
            p["first_seen"] = now()
            # only check keywords on new products. if i do it every run
            # it just alerts the same products over and over forever
            name_lower = p["name"].lower()
            for kw in keywords:
                if kw.lower() in name_lower:
                    msg = "Keyword match ({}): {} - {}".format(kw, p["name"], p["price"])
                    add_alert(alerts, p["url"], "keyword", msg)
        else:
            p["first_seen"] = old["first_seen"]
            # was sold out last time, now its in stock again
            if old["in_stock"] == 0 and p["in_stock"] == 1:
                msg = "Restock: {} is back in stock - {}".format(p["name"], p["price"])
                add_alert(alerts, p["url"], "restock", msg)
            # price went down
            if price_to_number(p["price"]) < price_to_number(old["price"]):
                msg = "Price drop: {} is now {} (was {})".format(
                    p["name"], p["price"], old["price"])
                add_alert(alerts, p["url"], "price", msg)
        p["last_seen"] = now()
        database.save_product(p)
    return alerts
