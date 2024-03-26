from flask import Blueprint, jsonify, request
from .auth_jwt import token_creator, token_verify

route_bp = Blueprint("route", __name__)


# Access with token validate. T-28min
@route_bp.route("/secret", methods=["GET"])
@token_verify
def secret_route():

    return jsonify({"data": "Mensagem secreta"}), 200


# Generate token with auth.
@route_bp.route("/auth", methods=["POST"])
def auth_gentoken_route():

    token = token_creator.create(uid=12)

    return jsonify({"token": token}), 200
