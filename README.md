# Výsledky z Googlu

Jednoduchá webová aplikace. Zadáš klíčová slova a dostaneš přirozené (organické) výsledky z první strany Googlu. Výsledky si můžeš uložit do souboru JSON.

Výsledky z Googlu se získávají přes službu [SerpApi](https://serpapi.com), protože Google automatické stahování blokuje.

## Jak to funguje

1. Na úvodní obrazovce zadáš přístupový token.
2. Napíšeš hledaný výraz a odešleš formulář.
3. Server zavolá SerpApi a z odpovědi vezme jen organické výsledky (reklamy ignoruje).
4. Stránka ukáže seznam výsledků. Tlačítkem **Uložit JSON** je stáhneš jako `vyhledavani_<výraz>.json`.

## Nastavení

Aplikace čte dvě proměnné prostředí. Nikdy je nepiš přímo do kódu.

| Proměnná | K čemu je |
|---|---|
| `SERPAPI_KEY` | klíč ze SerpApi (zdarma po registraci) |
| `ACCESS_TOKEN` | heslo pro vstup do aplikace; když není nastavené, aplikace je bez hesla (jen pro lokální vývoj) |

Počet hledání je omezený na 200 za měsíc (`MAX_SEARCHES` v `app/search.py`). Stejné hledání se hodinu pamatuje, takže opakované kliknutí na stejný výraz limit nečerpá.

## Spuštění lokálně

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
SERPAPI_KEY=tvuj_klic ACCESS_TOKEN=nejake_heslo .venv/bin/python wsgi.py
```

Aplikace poběží na http://localhost:3000.

## Testy

```bash
.venv/bin/pytest -v
```

Testy nevolají internet ani SerpApi, takže nespotřebují žádná hledání.

## Nasazení (např. Render)

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn wsgi:app`
- **Environment Variables:** `SERPAPI_KEY` a `ACCESS_TOKEN`

## Struktura projektu

```
app/
  __init__.py     sestaví aplikaci
  routes.py       adresy: přihlášení, hledání, stažení
  auth.py         kontrola přístupového tokenu
  search.py       volání SerpApi, výběr výsledků, měsíční limit
  export.py       název souboru pro uložení
  templates/      HTML stránky (login.html, index.html)
  static/         vzhled (style.css)
tests/            testy rozdělené podle modulů
wsgi.py           vstupní bod aplikace
```
