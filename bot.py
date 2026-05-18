# infobots - main script
# run "python bot.py --init" once, then "python bot.py --once" to check the stores

import argparse
import scraper
import checker
import database

# stores to watch (pointing at the mock store for now)
TARGETS = [
    {"url": "http://localhost:5000/", "store": "Demo Sneaker Store"},
]


def run_once():
    for t in TARGETS:
        print("checking", t["store"], "...")
        products = scraper.scrape(t["url"], t["store"])
        alerts = checker.check(products)
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
