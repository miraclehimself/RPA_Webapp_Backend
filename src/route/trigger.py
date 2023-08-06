from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.triggers import newTrigger, getTrigger
trigger = Blueprint("trigger", __name__, url_prefix="/trigger")


@trigger.get('/')
@jwt_required()
@swag_from('../docs/trigger/trigger.yaml')
def workspace_trigger():
  identity = get_jwt_identity()
  return getTrigger(identity['workspaceid'])


@trigger.post('/')
@jwt_required()
def new_trigger():
  identity = get_jwt_identity()
  return newTrigger(identity)
