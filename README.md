# InfoBots

> 🗄️ **A personal archive.** I built InfoBots through high school and college, from 2018 to 2024. This is that same project, kept runnable on a modern Python. Nothing here was rebuilt in 2026.

**Status:** Last maintained 2024. Archived in 2026 and kept runnable against a bundled mock store. Not under active development.

InfoBots is a set of Python monitoring bots that watch online sneaker stores for new products, restocks, and price drops, then post real-time alerts to a Discord server. I built the first version in high school to power a private sneaker-reselling community.

---

## About this archive

I stopped working on InfoBots around 2024, for a few reasons. Keeping the bots running took regular maintenance, and between school and other interests I didn't have the time for it anymore. The sneaker resale market had also cooled off a long way from its peak, and the resale margins that made a monitoring community worth running mostly weren't there anymore. So I gradually set the project down. In 2026 I came back to archive it properly:

- **Preserved, not rebuilt.** The monitoring engine, the alert logic and the overall structure are all original work. I didn't rewrite InfoBots in 2026.
- **Kept runnable.** I made only the smallest changes needed to run it on a current Python 3 toolchain. This was conservation, not a redesign.
- **Watches a bundled mock store, not live sites.** An archive should run for anyone who clones it, without firing requests at real retailer websites. The repo includes a small local "mock store" that behaves like the sites InfoBots was built to watch, so you can run the whole system end to end, self-contained, and still see real alerts fire.

---

## What it does

1. **Fetches** each store's page (HTML for most, a JSON feed for Shopify stores).
2. **Parses** out every product: name, price, in-stock status. Each store layout gets its own parser.
3. **Compares** the result against the previous run, stored in SQLite.
4. **Classifies** what changed: a new product, a restock, a price drop, or a name matching a watch keyword.
5. **Alerts** Discord through a webhook, or just prints to the console in dry-run mode.
6. **Repeats** on a loop in `--watch` mode.

---

## Architecture (as built, 2018–2024)

```
TARGETS: three stores, each with its own parser
   │
   ▼  requests.get()
scraper.py
   │  picks a parser based on the store
   ▼
parsers/nike.py  ·  parsers/footlocker.py  ·  parsers/shopify.py
   │  → name, price, in-stock
   ▼
checker.py  ──►  SQLite (data/infobots.db)   compares against the last run
   │
   ▼  new  ·  restock  ·  price drop  ·  keyword match
discord_alert.py  ──►  Discord webhook        (or --dry-run to the console)
```

---

## The stores it watches

The mock store ships three fake retailers, each laid out differently *on purpose*, so the bot needs a separate parser for each one, exactly like the real retailers did.

| Store | Endpoint | Format | Parser |
|---|---|---|---|
| Nike | `/nike` | HTML grid of product cards | `parsers/nike.py` |
| Foot Locker | `/footlocker` | HTML product list | `parsers/footlocker.py` |
| Solefly | `/solefly/products.json` | Shopify JSON feed | `parsers/shopify.py` |

---

## Setup

Needs Python 3. Install the libraries:

```bash
pip install -r requirements.txt
```

## Running it

Start the mock store in one terminal:

```bash
python3 mockstore/server.py
```

Then, in another terminal:

```bash
python3 bot.py --init            # set up the database (first time only)
python3 bot.py --once            # run one check
python3 bot.py --once --dry-run  # ...without touching Discord
```

| Command | What it does |
|---|---|
| `python3 bot.py --watch` | Keep checking on a loop |
| `python3 bot.py --export` | Write recent alerts to `drops.json` |

---

## Discord alerts

Copy `config.example.json` to `config.json` and drop in your webhook URL (Discord → Server Settings → Integrations → Webhooks). `config.json` is gitignored, so the URL never reaches GitHub. With no `config.json`, the bot simply skips Discord.

## Testing the alerts

The mock store has admin routes so you can change a store while the bot is running, then watch it react:

| Route | Effect |
|---|---|
| `/admin/<store>/restock/<id>` | Put a product back in stock |
| `/admin/<store>/soldout/<id>` | Mark a product sold out |
| `/admin/<store>/price/<id>/<price>` | Change a price |

`<store>` is `nike`, `footlocker`, or `solefly`. For example, open
`http://127.0.0.1:5000/admin/nike/restock/dunk-low-panda` in a browser, run `python3 bot.py --once` again, and you'll get a restock alert.

---

## The SneakerBro connection

`python3 bot.py --export` writes `drops.json`. My **SneakerBro** app, another project from the same era that I archived the same way, reads that file as its drop feed. The two early projects were built to plug into each other.

---

## Repository layout

```
infobots/
├── bot.py             entry point + the list of stores to watch
├── scraper.py         fetches a page, hands it to the right parser
├── parsers/           one parser per store layout
│   ├── nike.py            HTML product grid
│   ├── footlocker.py      HTML product list
│   └── shopify.py         products.json feed
├── checker.py         decides what's new / restocked / cheaper
├── database.py        SQLite storage
├── discord_alert.py   posts alerts to a Discord webhook
├── mockstore/         the three fake stores used for this archive
└── tests/             checks for the tricky parts (price parsing)
```

---

## Built with

- **Python 3**
- **requests + BeautifulSoup** for fetching and parsing store pages
- **Flask** for the mock store
- **SQLite** for storage, via the standard library
- **Discord webhooks** for alerts

No frameworks beyond these. It's a 2018-era project and the stack is kept honest to that.
