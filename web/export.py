"""Export výsledků do souboru."""
from werkzeug.utils import secure_filename


def file_name(query):
    """Z hledaného výrazu udělá bezpečný název souboru (bez diakritiky a mezer)."""
    word = secure_filename(query or "")
    return "vyhledavani_" + word + ".json" if word else "vyhledavani.json"
