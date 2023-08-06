from flask import request
from src.services.billing import subsriptionByWorkspace
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
def subscription(workspace_id):
  sub = subsriptionByWorkspace(workspace_id).as_dict()
  if sub:
    return {
      'msg': 'Workspace Subscription retrived successfuly',
      'data': sub
    }, HTTP_200_OK

  return {'msg': 'No subscription for workspace'}, HTTP_404_NOT_FOUND
