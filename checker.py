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
        p["last_seen"] = now()
        database.save_product(p)
    return alerts
