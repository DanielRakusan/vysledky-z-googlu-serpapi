"""Vstupní bod: lokálně `python app.py`, na hostingu (např. Render) `gunicorn app:app`."""
from web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=3000)
