from urllib.parse import urlencode
from flask import Blueprint, request, redirect, jsonify
from pkce import generate_pkce_pair
from config import FUSIONAUTH_BASE_URL
from .state import *

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/callback", methods=["GET"])
def callback():
    return jsonify({"ping": "/callback"})


@auth_blueprint.route("/login", methods=["GET"])
def login():
    new_state = state.push_redirect_url(
        request.args.get("redirect_uri"),
        request.args.get("state")
    )

    code_verifier, code_challenge = generate_pkce_pair()

    redirect_uri = "".join(
        [request.scheme, "://", request.host, "/auth/callback"]
    )

    query = urlencode({
        "response_type": "code",
        "scope": "openid offline_access",
        "client_id": request.args.get("client_id"),
        "state": new_state,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    })

    redirect_url = "".join(
        [FUSIONAUTH_BASE_URL, "/oauth2/authorize", "?", query])

    response = redirect(redirect_url, code=302)

    response.set_cookie(
        key="code_verifier",
        value=code_verifier,
        secure=True,
        httponly=True,
        samesite="lax"
    )
    return response


# @auth_blueprint.route("/logout", methods=["GET"])
# def logout():
#     return auth_controller.logout()


# @auth_blueprint.route("/refresh", methods=["POST"])
# def refresh():
#     return auth_controller.refresh()


# @auth_blueprint.route("/register", methods=["GET"])
# def register():
#     return auth_controller.register()


# @auth_blueprint.route("/user", methods=["GET"])
# def user():
#     return auth_controller.user()
