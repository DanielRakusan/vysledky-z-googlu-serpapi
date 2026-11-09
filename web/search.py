"""Vyhledávání: volání SerpApi, výběr organických výsledků a měsíční limit."""
import json
import os
import time
from datetime import date
from urllib.parse import quote
from urllib.request import urlopen

MAX_SEARCHES = 200  # největší počet hledání za měsíc
CACHE_SECONDS = 3600  # po tuto dobu se stejné hledání nevolá znovu
cache = {}  # hledaný výraz -> (čas uložení, výsledky)
searches_done = 0
counted_month = date.today().strftime("%Y-%m")


def parse_results(data):
    """Z odpovědi SerpApi vezme jen přirozené (organické) výsledky, reklamy ignoruje."""
    results = []
    for i, item in enumerate(data.get("organic_results", []), start=1):
        results.append({
            "position": i,
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })
    return results


def limit_reached(done, maximum):
    return done >= maximum


def search_google(q):
    url = ("https://serpapi.com/search.json?engine=google&q=" + quote(q)
           + "&api_key=" + os.environ["SERPAPI_KEY"])
    with urlopen(url, timeout=30) as response:
        return json.load(response)


def run_search(q):
    """Vrátí (výsledky, chybová zpráva). Počítá měsíční limit."""
    global searches_done, counted_month
    key = q.lower()
    saved = cache.get(key)
    if saved and time.time() - saved[0] < CACHE_SECONDS:
        return saved[1], ""  # stejné hledání nedávno proběhlo, limit se nečerpá
    month = date.today().strftime("%Y-%m")
    if month != counted_month:  # nový měsíc, počítadlo od nuly
        counted_month = month
        searches_done = 0
    if limit_reached(searches_done, MAX_SEARCHES):
        return None, "Limit hledání byl vyčerpán."
    if not os.environ.get("SERPAPI_KEY"):
        return None, "Chybí SERPAPI_KEY."
    searches_done += 1
    try:
        data = search_google(q)
    except Exception:
        return None, "Vyhledávání se nepovedlo."
    if "error" in data:
        return None, data["error"]
    results = parse_results(data)
    cache[key] = (time.time(), results)
    return results, ""
