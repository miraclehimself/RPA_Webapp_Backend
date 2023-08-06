import imp
from src.models.workspace import db, Workspace, WorkspaceUsers, TWSU
from src.models.user import User
from src.utils import serializeList, serializeData
def workspaceByName(name):
  return Workspace.query.filter_by(name=name).first()


def workspaceByUrl(url):
  return Workspace.query.filter_by(url=url).first()


def workspaceById(id):
  return Workspace.query.filter_by(id=id).first()


def addWorkspace(name, url):
  workspace = Workspace(name = name,url=url)
  db.session.add(workspace)
  db.session.commit()
  return workspace


def addWorkspaceUser(workspace, user, user_role):
  workspaceUser = WorkspaceUsers()
  workspaceUser.workspace = workspace
  workspaceUser.user_role = user_role
  workspaceUser.user_data = user
  db.session.add(workspaceUser)
  workspace.workspace_users.append(workspaceUser)
  db.session.add(workspace)
  db.session.commit()
  return workspaceUser
def removeWorkespaceUser(workspace_id, user_id):
  workspaceUser = WorkspaceUsers().query.filter_by(workspace_id=workspace_id, user_id=user_id).first()
  db.session.delete(workspaceUser)

def workspaceUserByEmail(workspace_id, useremail):
  # return users
  query = """
    SELECT fullname, email, password, workspace_id, user_id, user_role
    FROM "rpa-test".user u 
    JOIN "rpa-test".workspace_users w ON u.id = w.user_id
    WHERE w.workspace_id = :wi AND u.email = :ue;
  """
  data = db.session.execute(
      query,
      {'wi': workspace_id, 'ue': useremail}
  ).mappings().first()
  return serializeData(data)

def addTWSU(email, role, workspace_id):
  twsu = TWSU(email=email, role=role, workspace_id=workspace_id)
  db.session.add(twsu)
  db.session.commit()
  return twsu

def deleteTWSU(twsu):
  db.session.delete(twsu)
  db.session.commit()

def twsuById(id):
  return TWSU.query.filter_by(id=id).first()

def workspaceUserById(workspace_id, user_id):
  # return users
  query = """
    SELECT fullname, email, password, workspace_id, user_id, user_role
    FROM "rpa-test".user u 
    JOIN "rpa-test".workspace_users w ON u.id = w.user_id
    WHERE w.workspace_id = :wi AND u.id = :ui;
  """
  data = db.session.execute(
      query,
      {'wi': workspace_id, 'ui': user_id}
  ).mappings().first()
  return serializeData(data)


def editUserRole(workspace_id, user_id, role):
  ws = Workspace.query.filter_by(workspace_id=workspace_id, user_id = user_id).first()
  ws.user_role = role
  db.session.commit()
  return ws
