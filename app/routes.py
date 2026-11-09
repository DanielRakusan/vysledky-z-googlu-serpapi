"""Adresy aplikace: přihlášení, vyhledávání a stažení výsledků."""
import json

from flask import Blueprint, Response, redirect, render_template, request

from app.auth import expected_token, logged_in, token_ok
from app.export import file_name
from app.search import run_search

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    # přihlášení tokenem (formulář)
    if request.method == "POST":
        sent = request.form.get("token", "").strip()
        if token_ok(sent, expected_token()):
            response = redirect("/")
            response.set_cookie("token", sent, httponly=True)
            return response
        return render_template("login.html", message="Neplatný přístupový token.")

    if not logged_in():
        return render_template("login.html", message="")

    # hledání (formulář odešle ?q=...)
    q = request.args.get("q", "").strip()
    results, message = None, ""
    if q:
        results, message = run_search(q)
    if results is not None and not results:
        message = "Nic nenalezeno."
    data = json.dumps({"query": q, "results": results}, ensure_ascii=False, indent=2)
    return render_template("index.html", q=q, results=results,
                           message=message, data=data)


@main.route("/download", methods=["POST"])
def download():
    """Vrátí výsledky jako soubor vyhledavani_<hledaný výraz>.json."""
    if not logged_in():
        return Response("Přístup odepřen", 401)
    try:
        data = json.loads(request.form.get("data", ""))
    except ValueError:
        return Response("Neplatná data", 400)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(body, mimetype="application/json", headers={
        "Content-Disposition": "attachment; filename=" + file_name(data.get("query"))})
