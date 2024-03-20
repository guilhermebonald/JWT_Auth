from flask import Blueprint, jsonify, request
import jwt
from datetime import datetime, timedelta

route_bp = Blueprint("route", __name__)


# Access with token validate. T-28min
@route_bp.route("/secret", methods=["GET"])
def secret_route():

   

    return jsonify({"data": "Mensagem secreta"}), 200


# Generate token with auth.
@route_bp.route("/auth", methods=["POST"])
def auth_gentoken_route():

    return jsonify({"token": token}), 200
