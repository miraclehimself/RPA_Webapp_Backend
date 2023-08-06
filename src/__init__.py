from flask.json import jsonify
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask
from src.route import api
from src.models import db
from src.utils import CustomJSONEncoder
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.config.swagger import template, swagger_config
from src.config.config import config_by_name
from flask_cors import CORS

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(api)
    app.json_encoder = CustomJSONEncoder

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return {'error': 'Something went wrong, we are working on it'}, HTTP_500_INTERNAL_SERVER_ERROR

    return app
