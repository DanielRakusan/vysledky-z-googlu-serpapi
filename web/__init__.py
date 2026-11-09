"""Balíček aplikace: tady se aplikace sestavuje."""
from flask import Flask


def create_app():
    """Vytvoří a sestaví aplikaci."""
    app = Flask(__name__)

    from web.routes import main
    app.register_blueprint(main)

    return app
