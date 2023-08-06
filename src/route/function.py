
from flask import Blueprint
from flask_jwt_extended import  jwt_required
from flasgger import swag_from
from src.controllers.function import addFunction, allFunctions
function = Blueprint("function", __name__, url_prefix="/function")


@function.put('/add')
def addNew():
  return addFunction()


@function.get('/')
@jwt_required()
# @swag_from('../docs/scripts/scripts.yaml')
def getAll():
  return allFunctions()


# @script.post('/task')
# @jwt_required()
# # @swag_from('../docs/scripts/task.yaml')
# def task():
#   return buildScript()
