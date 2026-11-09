"""Testy kontroly přístupového tokenu."""
from web.auth import token_ok


def test_spravny_token_projde():
    assert token_ok("tajne", "tajne") is True


def test_spatny_nebo_chybejici_token_neprojde():
    assert token_ok("jiny", "tajne") is False
    assert token_ok(None, "tajne") is False


def test_bez_nastaveneho_tokenu_projde_vsechno():
    assert token_ok(None, None) is True
