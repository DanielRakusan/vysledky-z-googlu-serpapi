"""Vstupní bod: lokálně `python wsgi.py`, na hostingu `gunicorn wsgi:app`."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=3000)
