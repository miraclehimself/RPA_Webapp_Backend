from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.schedule import getSchedule
schedule = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule.get('/')
@jwt_required()
@swag_from('../docs/schedule/schedule.yaml')
def trigger():
  identity = get_jwt_identity()
  return getSchedule(identity['workspaceid'])
