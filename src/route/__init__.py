from flask import Blueprint

from .workspace import workspace
from .auth import auth
from .function import function
from .token import token
from .bot import bot
from .billing import billing
from .flow import flow
from .schedule import schedule
from .user import user
from .trigger import trigger

api = Blueprint("api", __name__, url_prefix="/api/v1")
api.register_blueprint(auth)
api.register_blueprint(function)
api.register_blueprint(token)
api.register_blueprint(bot)
api.register_blueprint(workspace)
api.register_blueprint(billing)
api.register_blueprint(flow)
api.register_blueprint(schedule)
api.register_blueprint(user)
api.register_blueprint(trigger)
