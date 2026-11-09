"""Společné nastavení testů."""
import pytest

from web import search


@pytest.fixture(autouse=True)
def vycistit_pamet_hledani():
    """Každý test začíná s prázdnou pamětí hledání."""
    search.cache.clear()
