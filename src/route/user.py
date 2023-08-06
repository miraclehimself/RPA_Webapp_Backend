from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.user import  getUser
user = Blueprint("user", __name__, url_prefix="/user")


@user.get('/')
@jwt_required()
@swag_from('../docs/user/user.yaml')
def workspace_user():
  identity = get_jwt_identity()
  return getUser(identity['workspaceid'])

