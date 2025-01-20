from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_file
import folium.features
import folium.folium
from app.models.tables import User
from datetime import datetime
import json
import requests
import os
import folium

from app.auth.auth import auth, get_google_provider_cfg, client, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID
from app.models.forms import Dep

from app.ext.db import db
from app.cache.cache import cache

from ..ultils import remove_file, create_map, user_message

#Import dos Controllers
from app.controllers.FiltroController import FiltroController
from app.controllers.DadosController import DadosController
from app.controllers.AIController import AIController
from app.controllers.PerfilController import PerfilController

bp_app = Blueprint("bp", __name__)

##
## Views
##

### Endpoint para download do backup, somente admin ###

@bp_app.route("/save-backup")
def backup():
    backup_file_path = "/home/HelpDeskPython/db.sqlite"
    
    try:
        if session["admin"]:
            if os.path.exists(backup_file_path):
                return send_file(backup_file_path, as_attachment=True)
            else:
                return "Arquivo de db nao encontrado", 404
        return "Sem permissao para accesar esta pagina", 404
    except KeyError:
        return "Sem permissao para accesar esta pagina", 404

##Endpoints para login
@bp_app.route("/login")
def init_login():
    request_uri = auth()
    return redirect(request_uri)

@bp_app.route("/login/get_user_info")
def get_user_info():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = {
        "id":unique_id, "nome":users_name, "email":users_email, "icon":picture
    }

    icon = user["icon"].split("/")[-1]
    
    # Send user back to homepage
    return redirect(url_for("bp.create_user", id=user["id"], email=user["email"], nome=user["nome"], icon=icon))

@bp_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("bp.login"))

@bp_app.route("/", methods=["GET", "POST"])
def login():
    try:
        if session["id"]:
            if PerfilController.is_allowed(session["id"]):
                if session["admin"]:
                    return redirect("/home-admin")
                return redirect("/home")
            else:
                return render_template("blocked_user.html")
    except KeyError:
        return render_template("login.html")

@bp_app.route("/home")
def index():
    try:
        if session["id"]:
            return render_template("index.html", admin=False)
    except KeyError:
        return redirect("/")

@bp_app.route("/home-admin")
def index_admin():
    if session["admin"]:
        return render_template("index.html", admin=True)
    else:
        return redirect("/")

########################
def configure(app):
    app.register_blueprint(bp_app)
