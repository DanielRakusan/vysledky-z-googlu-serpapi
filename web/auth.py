"""Přístupový token: kontrola, jestli je návštěvník přihlášený."""
import hmac
import os

from flask import request


def token_ok(sent, expected):
    """Když není token nastavený (lokální vývoj), pustí všechny. Jinak musí sedět."""
    if not expected:
        return True
    return hmac.compare_digest(sent or "", expected)


def expected_token():
    return os.environ.get("ACCESS_TOKEN")


def logged_in():
    return token_ok(request.cookies.get("token"), expected_token())
