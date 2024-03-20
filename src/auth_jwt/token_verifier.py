from flask import jsonify, request
import jwt
from .token_handler import token_creator


# min: 44:00
def token_verify(function: callable) -> callable:
    def decorated(*arg, **kwargs):
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
            return jsonify({"error": "Token Inválido"}), 401

        # validação de expiração do token
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token Expirado"}), 401

        # Se o token for gerado sem valor de "uid" cai nessa excessão
        except KeyError as e:
            return jsonify({"error": "Token Inválido2"}), 401

        if int(token_uid) != int(uid):
            return jsonify({"error": "User não permitido"}), 400

        next_token = token_creator.refresh(token)

        return function(next_token, *arg, **kwargs)
