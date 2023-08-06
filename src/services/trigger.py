from src.models.trigger import db, Trigger

def addTrigger(name, description, robot, flow, flow_version, type, item, properties, workspace):
  newTrigger = Trigger(name=name, description=description, robot=robot, flow=flow, trigger_type = type, trigger_item = item, trigger_properties=properties, workspace=workspace, flow_version=flow_version)
  db.session.add(newTrigger)
  db.session.commit()
  return newTrigger

def triggerByWorkspace(workspace_id):
  return Trigger.serialize_list(Trigger.query.filter_by(workspace_id=workspace_id).all())

