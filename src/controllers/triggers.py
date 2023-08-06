from pickle import TRUE
from flask import request
from src.services.bot import botByWorkspaceId, saveBotScript
from src.services.flows import flowByIdUser, flowData, flowDataByVersion
from src.services.trigger import addTrigger, triggerByWorkspace
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from src.services.workspace import workspaceById
from src.utils.script import flowScript, triggerScript


def getTrigger(workspace_id):
  return {
    'msg': 'Bot retrived successfully',
    'data': triggerByWorkspace(workspace_id)
  }, HTTP_200_OK


def newTrigger(identity):
  user_id = identity['userid']
  workspace_id = identity['workspaceid']
  name= request.json['name']
  description = request.json['description']
  robot_id = request.json['robot_id']
  flow_id =request.json['flow_id']
  flow_version = request.json['flow_version']
  trigger_type = request.json['trigger_type']
  trigger_item = request.json['trigger_item']
  trigger_properties = request.json['trigger_properties']

  workspace = workspaceById(workspace_id)

  if not workspace:
    return {'msg': "Something went wrong"}, HTTP_404_NOT_FOUND

  if not verifyTrigger(trigger_type, trigger_item, trigger_properties):
    return {'msg': "Invalid trigger data"}, HTTP_406_NOT_ACCEPTABLE

  flow = flowByIdUser(flow_id, user_id)
  if not flow:
    return {'msg': "Flow unaccessible"}, HTTP_401_UNAUTHORIZED

  flow_data = flowDataByVersion(flow.id, user_id, flow_version)
  if not flow_data:
    return {'msg': "Flow unaccessible"}, HTTP_401_UNAUTHORIZED
  
  

  robot = botByWorkspaceId(workspace_id, robot_id)
  if not robot:
    return {'msg': "Robot unaccessible"}, HTTP_401_UNAUTHORIZED

  if str(robot.status) != 'Disconnected' :
    return {'msg': "Robot unavailable"}, HTTP_405_METHOD_NOT_ALLOWED

  if (not flow_data.link ) or (not flow_data.nodes):
    return {'msg': "Error parsing flow"}, HTTP_406_NOT_ACCEPTABLE
  # if (flow_data.link and len(flow_data.link) < 1) or (flow_data.node and len(flow_data.nodes) < 2):
  #   return {'msg': "Error parsing flow"}, HTTP_406_NOT_ACCEPTABLE
  flow_script = flowScript(flow_data.link, flow_data.nodes)
  if not flow_script:
    return {'msg': "Error parsing flow"}, HTTP_406_NOT_ACCEPTABLE

  trigger_script = triggerScript({'type': trigger_type, 'item': trigger_item, 'property': trigger_properties}, flow_script)

  # Store to bot
  saveBotScript(robot, trigger_script)
  addTrigger(name, description, robot, flow,
                       flow_version, trigger_type, trigger_item, trigger_properties, workspace)

  return {
    "msg": "Operation successful",
    'data': triggerByWorkspace(workspace_id)
  }, HTTP_201_CREATED
  
def verifyTrigger(type, item, properties):
  return True

