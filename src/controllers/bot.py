from os import device_encoding
from flask import request
from src.services.billing import subsriptionByWorkspace
from src.services.bot import addBot, botByWorkspace, botByWorkspaceId, botByWorkspaceMac, deleteBot, disconnectBot, updateBot
# from src.services.user import getMachineById
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from src.services.workspace import workspaceById, workspaceByUrl

def getBots(workspace_id):
  bots = botByWorkspace(workspace_id)
  return {
    'msg': 'Bot retrived successfully',
    'data': bots
  }, HTTP_200_OK


def addBots(identity):
  workspace_id = identity['workspaceid']
  robot_name = request.json['robot_name']
  robot_type = request.json['robot_type']
  
  workspace = workspaceById(workspace_id)
  if not workspace:
    return {'msg': 'Workspace not found'}, HTTP_404_NOT_FOUND

  sub = subsriptionByWorkspace(workspace_id)
  if not sub:
    return {'msg': 'No billing information for this workspace'}, HTTP_404_NOT_FOUND

  if str(sub.status) != 'Active':
    return {'msg': 'No active billing information for this workspace'}, HTTP_401_UNAUTHORIZED
  bots = botByWorkspace(workspace_id)
  devBot = 0
  onDemand = 0
  prodBot = 0
  for bot in bots:
    if str(bot['type']) == 'Development':
      print('in here')
      devBot += 1
    elif str(bot['type']) == 'On Demand':
      onDemand += 1
    elif str(bot['type']) == 'Production':
      prodBot += 1
  if (robot_type == 'DEVELOPMENT' and devBot >= sub.dev_robot) or (robot_type == 'ON DEMAND' and onDemand >= sub.on_demand_robot) or (robot_type == 'PRODUCTION' and prodBot >= sub.prod_robot):
    return {'msg': f'{robot_type} robot limit exceeded'}, HTTP_400_BAD_REQUEST
  addBot(robot_name, 'DISCONNECTED', robot_type, workspace)
  return {
    'msg': 'Bot added successfully',
    'data': botByWorkspace(workspace_id)
  }, HTTP_201_CREATED


def delBot(bot_id, identity):
  bot = botByWorkspaceId(identity['workspaceid'], bot_id)
  if bot:
    deleteBot(bot)
    return {
      'msg': 'Bot deleted successfully',
      'data': botByWorkspace(identity['workspaceid'])
    }, HTTP_200_OK
  return {'msg': 'Bot not found'}, HTTP_404_NOT_FOUND


def patchBot(bot_id, identity):
  robot_name = request.json['robot_name']
  bot = botByWorkspaceId(identity['workspaceid'], bot_id)
  if bot:
    updateBot(bot, robot_name)
    return {
        'msg': 'Bot updated successfully',
        'data': botByWorkspace(identity['workspaceid'])
    }, HTTP_200_OK
  return {'msg': 'Bot not found'}, HTTP_404_NOT_FOUND

def botDisconnect(bot_id, identity):
  bot = botByWorkspaceId(identity['workspaceid'], bot_id)
  if bot:
    disconnectBot(bot)
    return {
        'msg': 'Bot disconnected successfully',
        'data': botByWorkspace(identity['workspaceid'])
    }, HTTP_200_OK
  return {'msg': 'Bot not found'}, HTTP_404_NOT_FOUND

def botMac(macid, identity):
  workspace_id = identity['workspaceid']
  mac_id = ""
  try:
    mac_id = identity['macid']
  except:
    return {'msg': 'Unauthorised'}, HTTP_401_UNAUTHORIZED
  if mac_id != macid:
    return {'msg': 'Unauthorised'}, HTTP_401_UNAUTHORIZED
  
  bots = botByWorkspaceMac(workspace_id)

  return { 'msg': 'success', 'data': bots}, HTTP_200_OK
