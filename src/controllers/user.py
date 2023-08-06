from flask import request
from datetime import datetime, timedelta
from src.services.workspace import addWorkspaceUser, deleteTWSU, workspaceById, workspaceUserByEmail, workspaceUserById, removeWorkespaceUser, addTWSU, twsuById
from src.services.user import addUserWorkspace, usersByWorkspace, userByMail
from src.services.billing import subsriptionByWorkspace
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

def getUser(workspace_id):
  return {
      'msg': 'Bot retrived successfully',
      'data': usersByWorkspace(workspace_id)
  }, HTTP_200_OK

