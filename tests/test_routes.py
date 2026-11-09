"""Testy celé aplikace: přihlášení, hledání a stažení."""
import pytest

from app import create_app, search


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN", "tajne")
    monkeypatch.setenv("SERPAPI_KEY", "x")
    return create_app().test_client()


def test_bez_tokenu_se_zobrazi_prihlaseni(client):
    html = client.get("/").get_data(as_text=True)
    assert "Přístupový token" in html
    assert "Zadej klíčová slova" not in html


def test_spatny_token_zustane_na_prihlaseni(client):
    html = client.post("/", data={"token": "spatne"}).get_data(as_text=True)
    assert "Neplatný přístupový token." in html


def test_se_spravnym_tokenem_se_zobrazi_vyhledavani(client):
    client.set_cookie("token", "tajne")
    html = client.get("/").get_data(as_text=True)
    assert "Zadej klíčová slova" in html


def test_vysledky_se_zobrazi_a_stahnou_jako_json(client, monkeypatch):
    monkeypatch.setattr(search, "search_google", lambda q: {
        "organic_results": [{"title": "Ahoj", "link": "https://a.cz", "snippet": "popis"}]})
    client.set_cookie("token", "tajne")
    html = client.get("/?q=test").get_data(as_text=True)
    assert "Ahoj" in html and "https://a.cz" in html
    odpoved = client.post("/download", data={"data": '{"query": "test", "results": []}'})
    assert odpoved.headers["Content-Disposition"] == "attachment; filename=vyhledavani_test.json"


def test_stazeni_bez_prihlaseni_je_zakazane(client):
    assert client.post("/download", data={"data": "{}"}).status_code == 401
