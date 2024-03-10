from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta

route_bp = Blueprint("route", __name__)


@route_bp.route("/secret", methods=["GET"])
def secret_route():

    raw_token = request.headers.get("Authorization")

    if not raw_token:
        return jsonify({"error": "Não Autorizado"}), 401

    return jsonify({"data": "Mensagem secreta"}), 200


@route_bp.route("/auth", methods=["POST"])
def authorization_route():
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=30)},
        key="1234",
        algorithm="HS256",
    )

    return jsonify({"token": token}), 200
