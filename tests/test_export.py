"""Testy názvu souboru pro uložení."""
from app.export import file_name


def test_nazev_souboru_podle_hledaneho_vyrazu():
    assert file_name("příliš žlutý kůň") == "vyhledavani_prilis_zluty_kun.json"
    assert file_name("") == "vyhledavani.json"
    assert file_name(None) == "vyhledavani.json"
