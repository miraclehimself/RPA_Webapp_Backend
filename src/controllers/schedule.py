from flask import request
from src.services.schedule import scheduleByWorkspace
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND


def getSchedule(workspace_id):
  return {
    'msg': 'Bot retrived successfully',
    'data': scheduleByWorkspace(workspace_id)
  }, HTTP_200_OK
