"""Testy vyhledávání: výběr výsledků a limit."""
from web import search
from web.search import limit_reached, parse_results


def test_vrati_organicke_vysledky_ve_spravnem_tvaru():
    data = {"organic_results": [
        {"title": "A", "link": "https://a.cz", "snippet": "popis A"},
        {"title": "B", "link": "https://b.cz"},
    ]}
    assert parse_results(data) == [
        {"position": 1, "title": "A", "link": "https://a.cz", "snippet": "popis A"},
        {"position": 2, "title": "B", "link": "https://b.cz", "snippet": ""},
    ]


def test_ignoruje_reklamy():
    data = {"ads": [{"title": "Reklama"}], "organic_results": [{"title": "A", "link": "https://a.cz"}]}
    result = parse_results(data)
    assert len(result) == 1
    assert result[0]["title"] == "A"


def test_bez_vysledku_vrati_prazdny_seznam():
    assert parse_results({}) == []


def test_limit_dotazu():
    assert limit_reached(49, 50) is False
    assert limit_reached(50, 50) is True


def test_run_search_vrati_vysledky(monkeypatch):
    monkeypatch.setenv("SERPAPI_KEY", "x")
    monkeypatch.setattr(search, "search_google", lambda q: {
        "organic_results": [{"title": "Ahoj", "link": "https://a.cz"}]})
    results, message = search.run_search("test")
    assert results[0]["title"] == "Ahoj"
    assert message == ""


def test_stejne_hledani_se_nevola_znovu(monkeypatch):
    monkeypatch.setenv("SERPAPI_KEY", "x")
    volani = []

    def falesne_hledani(q):
        volani.append(q)
        return {"organic_results": [{"title": "Ahoj", "link": "https://a.cz"}]}

    monkeypatch.setattr(search, "search_google", falesne_hledani)
    search.run_search("Test")
    search.run_search("test")
    assert len(volani) == 1
