from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta

route_bp = Blueprint("route", __name__)


# Access with token validate. T-28min
@route_bp.route("/secret", methods=["GET"])
def secret_route():

    # Get Token
    raw_token = request.headers.get("Authorization")
    uid = request.headers.get("uid")

    if not raw_token or not uid:
        return jsonify({"error": "Não Autorizado"}), 400

    """Se o token existir é preciso verificar a sua veracidade, já que ele deve ser unico,
    se não qualquer valor de token será usado para acessar o dado em questão."""
    try:
        token = raw_token.split()[1]
        token_information = jwt.decode(token, key="1234", algorithms="HS256")
        token_uid = token_information["uid"]
    except jwt.InvalidSignatureError:
        return jsonify({"error": "Token Invalido"}), 401

    # validação de expiração do token
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token Expirado"}), 401

    if int(token_uid) != int(uid):
        return jsonify({"error": "User não permitido"}), 400

    return jsonify({"data": "Mensagem secreta"}), 200


# Generate token with auth.
@route_bp.route("/auth", methods=["POST"])
def auth_gentoken_route():
    token = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(minutes=30), "uid": 12},
        key="1234",
        algorithm="HS256",
    )

    return jsonify({"token": token}), 200
