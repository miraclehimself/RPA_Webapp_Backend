from flask import Blueprint

from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.flow import addFL, deleteFD, deleteFl, getAllFlowData, getFlow, getFlowData, inviteFl, newFlowData, renameFL, saveFD, shareFl, updateFlowData
flow = Blueprint("flow", __name__, url_prefix="/flow")


@flow.get('/')
@jwt_required()
@swag_from('../docs/flow/flow.yaml')
def sub():
  identity = get_jwt_identity()
  return getFlow(identity)

@flow.get('/<uuid:flow_id>')
@jwt_required()
def fd(flow_id):
  identity = get_jwt_identity()
  return getAllFlowData(flow_id, identity)


@flow.post('/<uuid:flow_id>')
@jwt_required()
def new_fd(flow_id):
  identity = get_jwt_identity()
  return newFlowData(flow_id, identity)


@flow.patch('/<uuid:flow_id>/<uuid:flow_data_id>')
@jwt_required()
def update_fd(flow_id, flow_data_id):
  identity = get_jwt_identity()
  return updateFlowData(flow_id, flow_data_id, identity)


@flow.post('/<uuid:flow_id>/<uuid:flow_data_id>')
@jwt_required()
def save_fd(flow_id, flow_data_id):
  identity = get_jwt_identity()
  return saveFD(flow_id, flow_data_id, identity)


@flow.delete('/<uuid:flow_id>/<uuid:flow_data_id>')
@jwt_required()
def delete_fd(flow_id, flow_data_id):
  identity = get_jwt_identity()
  return deleteFD(flow_id, flow_data_id, identity)


@flow.post('/')
@jwt_required()
def new_fl():
  identity = get_jwt_identity()
  return addFL(identity)


@flow.post('/<uuid:flow_id>/share')
@jwt_required()
def share_fl(flow_id):
  identity = get_jwt_identity()
  return shareFl(flow_id, identity)


@flow.post('/<uuid:flow_id>/invite')
@jwt_required()
def invite_fl(flow_id):
  identity = get_jwt_identity()
  return inviteFl(flow_id, identity)

@flow.patch('/<uuid:flow_id>')
@jwt_required()
def update_fl(flow_id):
  identity = get_jwt_identity()
  return renameFL(flow_id, identity)


@flow.delete('/<uuid:flow_id>')
@jwt_required()
def delete_fl(flow_id):
  identity = get_jwt_identity()
  return deleteFl(flow_id, identity)
