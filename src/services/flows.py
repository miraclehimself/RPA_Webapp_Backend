from unicodedata import name
from src.models.flows import Flows, db, FlowData
from src.utils import serializeData, serializeList
def flowByWorkspace(workspace_id, user_id):
  flows = db.session.query(Flows).filter(Flows.workspace_id == workspace_id).filter((Flows.created_by == user_id)|(Flows.shared_type.in_(['PUBLIC', 'WORKSPACE']))|(Flows.shared_with.any(user_id))).all()
  return Flows.serialize_list(flows)


# def allWorkspaceFlows(workspace_id):
#   flows = db.session.query(Flows).filter(Flows.workspace_id == workspace_id).all()
#   return flows

def flowById(flow_id):
  return Flows.query.filter_by(id = flow_id).one()


def flowByIdUser(flow_id, user_id):
  flow = db.session.query(Flows).filter(Flows.id == flow_id).filter((Flows.created_by == user_id) | (
      Flows.shared_type.in_(['PUBLIC', 'WORKSPACE'])) | (Flows.shared_with.any(user_id))).first()
  return flow
def flowInvite(flow, invited_id):
  if flow.shared_with:
    flow.shared_with.append(invited_id)
  else:
    flow.shared_with = [invited_id]
  db.session.commit()
  return flow


def flowUninvite(flow, user_id):
  try:
    flow.shared_with.remove(user_id)
  except:
    pass
  db.session.commit()
  return flow
def flowShare(flow, share_type):
  flow.shared_type = share_type
  db.session.commit()
  return flow


def addFlow(created_by, workspace, shared_type='PRIVATE', name='Untitled'):
  flow = Flows(name=name, created_by=created_by,
               workspace=workspace, shared_type=shared_type, versions=1)
  db.session.add(flow)
  db.session.commit()
  flowData = FlowData(flow=flow, flow_name=flow.name, name='Master', version=1)
  db.session.add(flowData)
  db.session.commit()
  return {**flow.as_dict()}

def renameFlow(flow, name):
  print(flow)
  flow.name = name
  db.session.commit()
  return flow

def deleteFlow(flow):
  db.session.delete(flow)
  db.session.commit()


def flowData(flowdata_id, user_id):
  fd = db.session.query(FlowData).join(Flows, FlowData.flow_id == Flows.id).filter(FlowData.id == flowdata_id).filter((Flows.created_by == user_id) | (
      Flows.shared_type.in_(['PUBLIC', 'WORKSPACE'])) | (Flows.shared_with.any(user_id))).order_by(FlowData.version.desc()).one()
  return fd

def flowDataByVersion(flow_id, user_id, version):
  fd = db.session.query(FlowData).filter((FlowData.flow_id == flow_id) & (FlowData.version == version)).filter((Flows.created_by == user_id) | (
      Flows.shared_type.in_(['PUBLIC', 'WORKSPACE'])) | (Flows.shared_with.any(user_id))).one()
  return fd

def allFlowData(flow_id, user_id):
  fd = db.session.query(FlowData).join(Flows, FlowData.flow_id == Flows.id).filter(
      Flows.id == flow_id).filter((Flows.created_by == user_id) | (
          Flows.shared_type.in_(['PUBLIC', 'WORKSPACE'])) | (Flows.shared_with.any(user_id))).order_by(FlowData.version.desc()).order_by(FlowData.version.desc()).all()
  return FlowData.serialize_list(fd)

def addFlowData(flow, name, description):
  recentVersion = FlowData.query.filter_by(flow_id=flow.id).order_by(FlowData.version.desc()).first()
  version = recentVersion.version + 1
  flowData = FlowData(flow=flow, name=name, flow_name=flow.name, description=description, version=version)
  flow.versions += 1
  db.session.add(flowData)
  db.session.commit()
  return allFlowData(flow.id, flow.created_by)


def saveFlowData(flow, flow_data_id, nodes, link):
  fd = FlowData.query.filter_by(id=flow_data_id, flow_id=flow.id).one()
  fd.link = link
  fd.nodes = nodes
  db.session.commit()
  return fd

def editFlowData(flow, flow_data_id, name, description):
  fd = FlowData.query.filter_by(id=flow_data_id, flow_id = flow.id).one()
  fd.name =name
  fd.description = description
  db.session.commit()
  return allFlowData(flow.id, flow.created_by)


def deleteFlowData(flow, flow_data_id):
  flow_id = flow.id
  fd = FlowData.query.filter_by(id=flow_data_id, flow_id=flow_id).one()
  flow.versions -= 1
  db.session.delete(fd)
  db.session.commit()
  return allFlowData(flow.id, flow.created_by)

def saveFlowDesign():
  pass
