from src.models.schedule import Schedule, db

def scheduleByWorkspace(workspace_id):
  schedules = Schedule.query.filter_by(workspace_id=workspace_id).all()
  return Schedule.serialize_list(schedules)