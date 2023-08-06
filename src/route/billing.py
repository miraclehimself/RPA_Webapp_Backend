from flask import Blueprint

from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.billing import subscription
billing = Blueprint("billing", __name__, url_prefix="/billing")

@billing.get('/subscription')
@jwt_required()
@swag_from('../docs/billing/subscription.yaml')
def sub():
  identity = get_jwt_identity()
  return subscription(identity['workspaceid'])
