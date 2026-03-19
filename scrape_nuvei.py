#!/usr/bin/env python3
"""
Scrapes Nuvei individual APM detail pages for card schemes
and saves them to data/ for parsing.
"""
import urllib.request
import time
import os

CARD_SCHEMES = [
    "visa",
    "mastercard",
    "american-express",
    "unionpay",
    "cartes-bancaires",
    "diners-discover",
    "elo",
    "rupay",
    "bancontact-card",
    "postfinance-card",
    "troy",
    "hipercard",
    "argencard",
    "cabal",
    "naranja",
    "south-korea-local-cards",
    "local-payments-africa--cards",
    "local-brazilian-credit-card-ips",
    "mastercard-send",
    "visa-direct",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "nuvei_apm_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch(slug):
    url = f"https://www.nuvei.com/apm/{slug}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")

for slug in CARD_SCHEMES:
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    if os.path.exists(out_path):
        print(f"  [skip] {slug} (already saved)")
        continue
    try:
        print(f"  Fetching /apm/{slug} ...", end=" ", flush=True)
        html = fetch(slug)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"saved ({len(html)//1024}KB)")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(1.5)   # polite delay

print(f"\nDone. Files saved to: {OUTPUT_DIR}")
