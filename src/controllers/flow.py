from flask import request
from src.models import workspace
from src.services.flows import addFlow, deleteFlow, deleteFlowData, editFlowData, flowByIdUser, flowByWorkspace, flowData, allFlowData, addFlowData, flowInvite, flowShare, renameFlow, saveFlowData
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
from src.services.user import userById
from src.services.workspace import workspaceById

def getFlow(identity):

  flow = flowByWorkspace(identity['workspaceid'], identity['userid'])
  return {
      "msg": "Workspace flow retrived",
      "data": flow
  }, HTTP_200_OK


def getFlowData(flow_id, identity):
  fd = flowData(flow_id, identity['userid'])
  if not fd:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  return {
      "msg": "Flow data retrived",
      "data": fd.as_dict()
  }, HTTP_200_OK


def getAllFlowData(flow_id, identity):
  fd = allFlowData(flow_id, identity['userid'])
  if not fd:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  return {
      "msg": "Flow data retrived",
      "data": fd
  }, HTTP_200_OK


def newFlowData(flow_id, identity):
  name = request.json['name']
  description = request.json['description']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  fd = addFlowData(flow, name, description)
  return {
      "msg": "Flow data retrived",
      "data": fd
  }, HTTP_201_CREATED

def updateFlowData(flow_id, flow_data_id, identity):
  name = request.json['name']
  description = request.json['description']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  fd = editFlowData(flow, flow_data_id, name, description)
  return {
      "msg": "Flow data updated",
      "data": fd
  }, HTTP_200_OK


def deleteFD(flow_id, flow_data_id, identity):
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  if flow.versions < 2:
    return {'msg': 'You must have at least 1 flow version'}, HTTP_403_FORBIDDEN
  fd = deleteFlowData(flow, flow_data_id)
  return {
      "msg": "Flow data deleted",
      "data": fd
  }, HTTP_200_OK

#save flow data
def saveFD(flow_id, flow_data_id, identity):
  link = request.json['link']
  nodes = request.json['nodes']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  fd = saveFlowData(flow, flow_data_id, nodes, link)
  return {
      "msg": "Flow data saved",
      "data": fd.as_dict()
  }, HTTP_200_OK



# Flows
def addFL(identity):
  name = request.json['name']
  workspace = workspaceById(identity['workspaceid'])
  fl = addFlow(identity['userid'], workspace, name=name)

  return {
      "msg": "Flow created",
      "data": fl
  }, HTTP_201_CREATED

def renameFL(flow_id, identity):
  name = request.json['name']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  print(flow)
  fl = renameFlow(flow, name)
  return {
      "msg": "Flow renamed",
      "data": fl.as_dict()
  }, HTTP_200_OK

def shareFl(flow_id, identity):
  shared_type = request.json['share_type']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  fl = flowShare(flow, shared_type)
  return {
      "msg": "Flow updated",
      "data": fl.as_dict()
  }, HTTP_200_OK


def inviteFl(flow_id, identity):
  user_id = request.json['user_id']
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  print(flow.shared_type)
  if str(flow.shared_type) != 'Private':
    return {'msg': 'Flow is not private'}, HTTP_405_METHOD_NOT_ALLOWED
  fl = flowInvite(flow, user_id)
  return {
    "msg": "Flow updated",
    "data": fl.as_dict()
  }, HTTP_200_OK

def deleteFl(flow_id, identity):
  flow = flowByIdUser(flow_id, identity['userid'])
  if not flow:
    return {'msg': 'No flow found'}, HTTP_404_NOT_FOUND
  deleteFlow(flow)
  return {
      "msg": "Flow deleted",
      "data": flowByWorkspace(identity['workspaceid'], identity['userid'])
  }, HTTP_200_OK
# delete, invite, share, rename, add
