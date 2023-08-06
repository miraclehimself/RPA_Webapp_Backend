from flask import request
import json
from src.services.billing import subsriptionByWorkspace
from src.services.workspace import addTWSU, addWorkspaceUser, deleteTWSU, removeWorkespaceUser, twsuById, workspaceById, workspaceUserById, workspaceById
from src.services.user import addUserWorkspace, userByMail, usersByWorkspace, usersByWorkspace
from src.services.flows import flowByWorkspace
from src.services.bot import botByWorkspace
from src.services.schedule import scheduleByWorkspace
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY

def workspaceStat(identity):
  workspace = workspaceById(identity['workspaceid'])
  if workspace:
    robots = botByWorkspace(identity['workspaceid'])
    robots_summary = {
      'development': {
        'count': 0,
        'connected': 0
      },
      'on_demand': {
        'count': 0,
        'connected': 0
      },
      'production': {
        'count': 0,
        'connected': 0
      }
    }
    for robot in robots:
      print(robot)
      if str(robot['type']) == 'Development':
        robots_summary['development']['count'] += 1
        if robot['status'] == 'Connected':
          robots_summary['development']['connected'] += 1
      elif str(robot['type']) == 'On Demand':
        robots_summary['on_demand']['count'] += 1
        if robot['status'] == 'Connected':
          robots_summary['On_demand']['connected'] += 1

      elif str(robot['type']) == 'Production':
        robots_summary['production']['count'] += 1
        if robot['status'] == 'Connected':
          robots_summary['production']['connected'] += 1
    sub = subsriptionByWorkspace(identity['workspaceid']).as_dict()
    users_summary = {
      'owner': 0,
      'admin': 0,
      'member': 0,
      'limit': sub['user_limit']
    }
    users = usersByWorkspace(identity['workspaceid'])
    for user in users:
      if user['user_role'] == 'OWNER':
        users_summary['owner'] += 1
      elif user['user_role'] == 'ADMIN':
        users_summary['admin'] += 1
      elif user['user_role'] == 'MEMBER':
        users_summary['member'] += 1
      
    return {
      "msg": "Workspace stat retrived",
      "data":{
        "flows": flowByWorkspace(identity['workspaceid'], identity['userid']),
        "robots": robots,
        "robots_summary": robots_summary,
        "schedules": scheduleByWorkspace(identity['workspaceid']),
        "users": users,
        "users_summary": users_summary
      }
    }
  return {'msg': 'Workspace data not found'}, HTTP_404_NOT_FOUND


def deleteUser(user_id, identity):
  if identity['userrole'] != 'OWNER' and identity['userrole'] != 'ADMIN':
    return {'msg': 'User not allowed to perform this operation'}, HTTP_401_UNAUTHORIZED

  admin = workspaceUserById(identity['workspaceid'], identity['userid'])
  print(admin)
  if not admin:
    return {'msg': 'User not allowed to perform this operation'}, HTTP_401_UNAUTHORIZED

  olduser = workspaceUserById(identity['workspaceid'], user_id)

  if not olduser:
    {'msg': 'Cannot find user'}, HTTP_404_NOT_FOUND
  if (olduser['user_role'] == 'ADMIN' and admin['user_role'] != 'OWNER') or olduser['user_role'] == 'OWNER':
    return {'msg': 'User not allowed to perform this operation'}, HTTP_401_UNAUTHORIZED

  removeWorkespaceUser(identity['workspaceid'], user_id)
  # To do: Add function to delete user from all wokspace flow
  return {'msg': 'Operation successful'}


def inviteUser(identity):
  user_email = request.json['email']
  user_role = request.json['user_role']
  workspace_id = identity['workspaceid']
  if identity['userrole'] != 'OWNER' and identity['userrole'] != 'ADMIN':
    return {'msg': 'User not allowed to perform this operation'}, HTTP_401_UNAUTHORIZED
  invitedUser = userByMail(user_email)
  if not invitedUser:
    return {'msg': 'User not found'}, HTTP_404_NOT_FOUND
  sub = subsriptionByWorkspace(workspace_id)

  if not sub:
    return {'msg': 'No billing information for this workspace'}, HTTP_404_NOT_FOUND
  print(sub.status)
  if str(sub.status) != 'Active':
    return {'msg': 'No active billing information for this workspace'}, HTTP_401_UNAUTHORIZED

  currentUsers = usersByWorkspace(workspace_id)
  for user in currentUsers:
    if user.user_id == invitedUser.id:
      return {'msg': 'User already in workspace'}, HTTP_405_METHOD_NOT_ALLOWED
  if not (len(currentUsers) < sub.user_limit):
    return {'msg': 'Workspace has reached its user limit'}, HTTP_401_UNAUTHORIZED

  twsu = addTWSU(user_email, user_role, workspace_id)
  return {'msg': 'Invitation sent', 'id': twsu.id}, HTTP_200_OK


def acceptInvite():
  inviteId = request.json['invite_id']
  invite = twsuById(inviteId)
  if not invite:
    return {'msg': 'Invite cannot be found'}, HTTP_404_NOT_FOUND
  sub = subsriptionByWorkspace(invite.workspace_id)

  if not sub:
    return {'msg': 'No billing information for this workspace'}, HTTP_404_NOT_FOUND

  if str(sub.status) != 'Active':
    return {'msg': 'No active billing information for this workspace'}, HTTP_401_UNAUTHORIZED
  user = userByMail(invite.email)
  currentUsers = usersByWorkspace(invite.workspace_id)
  for user in currentUsers:
    if user.user_id == user.id:
      return {'msg': 'User already in workspace'}, HTTP_405_METHOD_NOT_ALLOWED
  if not (len(currentUsers) < sub.user_limit):
    return {'msg': 'Workspace has reached its user limit'}, HTTP_401_UNAUTHORIZED
  workspace = workspaceById(invite.workspace_id)
  workspace_user = addWorkspaceUser(workspace, user, invite.role)
  user = addUserWorkspace(user, workspace_user)

  deleteTWSU(invite)

  return {'msg': 'Invitation accepted'}, HTTP_200_OK
