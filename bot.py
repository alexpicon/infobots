# infobots - main script
# run "python bot.py --init" once, then "python bot.py --once" to check the stores

import argparse
import json
import time
import scraper
import checker
import database
import discord_alert

# stores to watch. each one has a parser (see the parsers/ folder).
# note: use 127.0.0.1 not localhost, localhost was giving me empty pages
TARGETS = [
    {"store": "Nike", "url": "http://127.0.0.1:5000/nike", "parser": "nike"},
    {"store": "Foot Locker", "url": "http://127.0.0.1:5000/footlocker", "parser": "footlocker"},
    {"store": "Solefly", "url": "http://127.0.0.1:5000/solefly/products.json", "parser": "shopify"},
]

# product names with these words in them get a keyword alert
KEYWORDS = ["yeezy", "jordan 1", "panda"]

# how many seconds to wait between checks in watch mode
CHECK_EVERY = 60


def run_once(dry_run=False):
    for t in TARGETS:
        print("checking", t["store"], "...")
        try:
            products = scraper.scrape(t)
        except Exception as e:
            # one store being down or changing its layout shouldn't stop
            # the rest from getting checked (matters most in watch mode)
            print("  couldn't check {}: {}".format(t["store"], e))
            continue
        alerts = checker.check(products, KEYWORDS)
        if alerts:
            for a in alerts:
                print("  ALERT:", a["message"])
                discord_alert.send(a["message"], dry_run)
        else:
            print("  nothing new")


def export_drops():
    # dumps the alerts to a json file so my sneakerbro app can show them
    # as a drop feed instead of me copying stuff over by hand
    alerts = database.get_alerts()
    drops = []
    for a in alerts:
        product = database.get_product(a["url"])
        drops.append({
            "type": a["type"],
            "name": product["name"] if product else "",
            "store": product["store"] if product else "",
            "price": product["price"] if product else "",
            "time": a["time"],
        })
    with open("drops.json", "w") as f:
        json.dump(drops, f, indent=2)
    print("wrote", len(drops), "drops to drops.json")


def watch(dry_run=False):
    print("watch mode - checking every", CHECK_EVERY, "seconds (ctrl+c to stop)")
    while True:
        run_once(dry_run)
        time.sleep(CHECK_EVERY)


def main():
    parser = argparse.ArgumentParser(description="infobots store monitor")
    parser.add_argument("--init", action="store_true", help="create the database")
    parser.add_argument("--once", action="store_true", help="check the stores one time")
    parser.add_argument("--watch", action="store_true",
                        help="keep checking the stores on a loop")
    parser.add_argument("--dry-run", action="store_true",
                        help="dont actually send to discord, just print the alerts")
    parser.add_argument("--export", action="store_true",
                        help="export the alerts to drops.json")
    args = parser.parse_args()

    if args.init:
        database.init_db()
    elif args.once:
        run_once(args.dry_run)
    elif args.watch:
        watch(args.dry_run)
    elif args.export:
        export_drops()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
