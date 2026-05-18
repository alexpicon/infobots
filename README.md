# InfoBots

bots that watch online stores for new products, restocks and price drops
and post alerts to a discord server.

i originally built this in high school (around 2018) and kept adding to it
through college until about 2024. back then it ran against real sneaker sites
and sent drops to a private discord i ran for a small reselling community.

## about this re-archive

this is a cleaned up version i put back together in 2026 so it actually runs
today. the main change: it no longer scrapes real stores. it points at a small
fake store ("mock store") that ships with the repo. scraping real sites gets you
blocked and is against their terms, and none of it is needed to show how the bot
works - the new product / restock / price / keyword logic is exactly the same.

everything else is basically how i had it: sqlite for storage, requests +
beautifulsoup for scraping, discord webhooks for alerts.

## what it does

- finds products it hasn't seen before -> "new" alert
- notices when a sold out product comes back -> "restock" alert
- notices when a price goes down -> "price drop" alert
- matches product names against a keyword list -> "keyword" alert
- saves everything to sqlite so it remembers between runs
- sends alerts to discord, or just prints them in dry run mode

## setup

needs python 3. install the libraries:

    pip install -r requirements.txt

## running it

start the mock store in one terminal:

    python mockstore/server.py

then in another terminal set up the database:

    python bot.py --init

and run a check:

    python bot.py --once

use --dry-run if you don't want it touching discord:

    python bot.py --once --dry-run

other commands:

    python bot.py --watch     keep checking on a loop
    python bot.py --export    write the alerts out to drops.json

## discord alerts

copy config.example.json to config.json and put your webhook url in it.
config.json is gitignored so the url doesn't end up on github. if there's no
config.json the bot just skips discord.

## testing the alerts

the mock store has a few routes so you can change it while the bot is running:

    /admin/restock/<slug>        put something back in stock
    /admin/soldout/<slug>        mark something sold out
    /admin/price/<slug>/<price>  change a price

for example, open http://127.0.0.1:5000/admin/price/yeezy-350-zebra/180 in a
browser, then run the bot again and you'll get a price drop alert.

## the sneakerbro connection

`python bot.py --export` writes drops.json. my SneakerBro app reads that file to
show a drop feed, so the two projects plug into each other.

## tests

    python tests/test_checker.py

## files

    bot.py            main script / command line
    scraper.py        fetches and parses store pages
    checker.py        works out what's new / restocked / cheaper
    database.py       sqlite stuff
    discord_alert.py  sends alerts to discord
    mockstore/        the fake store to test against
