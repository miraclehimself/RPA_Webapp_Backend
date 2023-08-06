from tokenize import group
from flask import request
from src.services.function import updateFuncs, getFunc
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

def addFunction():
  data = updateFuncs()
  return {'msg': 'Added successfullly', 'data': data}, HTTP_201_CREATED


def allFunctions():
  data = getFunc()
  return {'msg': 'Retrived successfully', 'data': data}, HTTP_200_OK


# def buildScript():
#   task_list = request.json['task_list']
#   valid = validateTaskList(task_list)
#   if valid == 'OK':
#     genBotScript(task_list)
#     return {'msg': 'Bot created successfully'}, HTTP_200_OK
#   else:
#     return {'msg': valid}, HTTP_400_BAD_REQUEST