# infobots - main script
# run "python bot.py --init" once, then "python bot.py --once" to check the stores

import argparse
import time
import scraper
import checker
import database
import discord_alert

# stores to watch (pointing at the mock store for now)
# note: use 127.0.0.1 not localhost, localhost was giving me empty pages
TARGETS = [
    {"url": "http://127.0.0.1:5000/", "store": "Demo Sneaker Store"},
]

# product names with these words in them get a keyword alert
KEYWORDS = ["yeezy", "jordan 1", "panda"]

# how many seconds to wait between checks in watch mode
CHECK_EVERY = 60


def run_once(dry_run=False):
    for t in TARGETS:
        print("checking", t["store"], "...")
        products = scraper.scrape(t["url"], t["store"])
        alerts = checker.check(products, KEYWORDS)
        if alerts:
            for a in alerts:
                print("  ALERT:", a["message"])
                discord_alert.send(a["message"], dry_run)
        else:
            print("  nothing new")


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
    args = parser.parse_args()

    if args.init:
        database.init_db()
    elif args.once:
        run_once(args.dry_run)
    elif args.watch:
        watch(args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
