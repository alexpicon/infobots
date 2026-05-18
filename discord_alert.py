# sends alert messages to my discord server using a webhook
# the webhook url goes in config.json which is gitignored so i dont leak it

import json
import os
import requests

CONFIG_PATH = "config.json"


def get_webhook_url():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    return cfg.get("webhook_url")


def send(message):
    url = get_webhook_url()
    if not url:
        print("  (no webhook in config.json, not sending to discord)")
        return
    try:
        requests.post(url, json={"content": message}, timeout=10)
    except Exception as e:
        print("  couldnt send to discord:", e)
