
from flask import Blueprint

from flasgger import swag_from
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from src.constants.http_status_codes import HTTP_200_OK
token = Blueprint("token", __name__, url_prefix="/token")

@token.get('/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
  identity = get_jwt_identity()
  token = create_access_token(identity=identity)
  return {'msg': 'New access token created', 'token': token}, HTTP_200_OK