# infobots - main script
# run "python bot.py --init" once, then "python bot.py --once" to check the stores

import argparse
import scraper
import checker
import database

# stores to watch (pointing at the mock store for now)
# note: use 127.0.0.1 not localhost, localhost was giving me empty pages
TARGETS = [
    {"url": "http://127.0.0.1:5000/", "store": "Demo Sneaker Store"},
]

# product names with these words in them get a keyword alert
KEYWORDS = ["yeezy", "jordan 1", "panda"]


def run_once():
    for t in TARGETS:
        print("checking", t["store"], "...")
        products = scraper.scrape(t["url"], t["store"])
        alerts = checker.check(products, KEYWORDS)
        if alerts:
            for a in alerts:
                print("  ALERT:", a["message"])
        else:
            print("  nothing new")


def main():
    parser = argparse.ArgumentParser(description="infobots store monitor")
    parser.add_argument("--init", action="store_true", help="create the database")
    parser.add_argument("--once", action="store_true", help="check the stores one time")
    args = parser.parse_args()

    if args.init:
        database.init_db()
    elif args.once:
        run_once()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
