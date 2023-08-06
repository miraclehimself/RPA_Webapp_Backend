
from flask import Blueprint

from flasgger import swag_from
from src.controllers.workspace import acceptInvite, deleteUser, inviteUser, workspaceStat
from flask_jwt_extended import jwt_required, get_jwt_identity
workspace = Blueprint("workspace", __name__, url_prefix="/workspace")

@workspace.get('/stat')
@jwt_required()
@swag_from('../docs/workspace/stat.yaml')
def stat():
  identity = get_jwt_identity()
  return workspaceStat(identity)


@workspace.delete('/user/<uuid:user_id>')
@jwt_required()
# @swag_from('../docs/user/user.yaml')
def remove_workspace_user(user_id):
  identity = get_jwt_identity()
  return deleteUser(user_id, identity)


@workspace.put('/invite')
@jwt_required()
# @swag_from('../docs/user/user.yaml')
def invite_workspace_user():
  identity = get_jwt_identity()
  return inviteUser(identity)


@workspace.post('/invite/accept')
# @jwt_required()
# @swag_from('../docs/user/user.yaml')
def workspace_user_accept():
  return acceptInvite()
