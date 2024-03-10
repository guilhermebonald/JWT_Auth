from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta

route_bp = Blueprint("route", __name__)


# Access with token validate.
@route_bp.route("/secret", methods=["GET"])
def secret_route():

    raw_token = request.headers.get("Authorization")

    if not raw_token:
        return jsonify({"error": "Não Autorizado"}), 401

    try:
        token = raw_token.split()[1]
        token_information = jwt.decode(token, key="1234", algorithms="HS256")
    except jwt.InvalidSignatureError:
        return jsonify({"error": "Token Invalido"}), 401

    return jsonify({"data": "Mensagem secreta"}), 200


# Generate token with auth.
@route_bp.route("/auth", methods=["POST"])
def auth_gentoken_route():
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=30)},
        key="1234",
        algorithm="HS256",
    )

    return jsonify({"token": token}), 200
