# compares whats on the store right now vs what we saw last time
# returns a list of alerts for the bot to send out

import datetime
import database


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def check(products):
    alerts = []
    for p in products:
        old = database.get_product(p["url"])
        if old is None:
            # never seen this product before
            msg = "New product: {} - {}".format(p["name"], p["price"])
            alerts.append({"url": p["url"], "type": "new", "message": msg})
            database.log_alert(p["url"], "new", msg)
            p["first_seen"] = now()
        else:
            p["first_seen"] = old["first_seen"]
            # was sold out last time, now its in stock again
            if old["in_stock"] == 0 and p["in_stock"] == 1:
                msg = "Restock: {} is back in stock - {}".format(p["name"], p["price"])
                alerts.append({"url": p["url"], "type": "restock", "message": msg})
                database.log_alert(p["url"], "restock", msg)
        p["last_seen"] = now()
        database.save_product(p)
    return alerts
