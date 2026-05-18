# all the database stuff goes here
# using sqlite so i dont have to run a server

import sqlite3
import datetime

DB_PATH = "data/infobots.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        url TEXT PRIMARY KEY,
        name TEXT,
        store TEXT,
        price TEXT,
        in_stock INTEGER,
        first_seen TEXT,
        last_seen TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        type TEXT,
        message TEXT,
        time TEXT
    )""")
    conn.commit()
    conn.close()
    print("database ready")


def get_product(url):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE url = ?", (url,))
    row = c.fetchone()
    conn.close()
    return row


def save_product(p):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO products
        (url, name, store, price, in_stock, first_seen, last_seen)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (p["url"], p["name"], p["store"], p["price"], p["in_stock"],
         p["first_seen"], p["last_seen"]))
    conn.commit()
    conn.close()


def log_alert(url, atype, message):
    conn = get_conn()
    c = conn.cursor()
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO alerts (url, type, message, time) VALUES (?, ?, ?, ?)",
              (url, atype, message, t))
    conn.commit()
    conn.close()
