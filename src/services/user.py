from src.models.user import db, User, TempUser, Machine
from src.utils import serializeList

def userByMail(email):
  return User.query.filter_by(email=email).first()

def userById(id):
  return User.query.filter_by(id=id).first()

def usersByWorkspace(id):
  # users = User.query.join(WorkspaceUsers).filter(User.workspaces.any(workspace_id=id)).all()
  # return User.serialize_list(users)
  # return users
  query = """
    SELECT fullname, email, user_id, user_role
    FROM "rpa-test".user u 
    JOIN "rpa-test".workspace_users w ON u.id = w.user_id
    WHERE w.workspace_id = :wi;
  """
  data = db.session.execute(
      query,
      {'wi': id}
  ).mappings().all()
  return serializeList(data)

def addUser(fullname, password, email):
  user = User(fullname=fullname, password = password, email=email)
  db.session.add(user)
  db.session.commit()
  return user

def addUserWorkspace(user, workspace):
  user.workspaces.append(workspace)
  db.session.commit()
  return user

def addTempUser(fullname, otp, email):
  user = TempUser(fullname=fullname, otp=otp, email=email)
  db.session.add(user)
  db.session.commit()
  return user
def deleteTempUser(user):
  db.session.delete(user)
  db.session.commit()

def tempUser(id):
  return TempUser.query.filter_by(id=id).first()

def validateTempUser(user):
  user.verified = True
  db.session.commit()
  return user


def getMachineByUser(user_id):
  return Machine.query.filter_by(user_id = user_id).first()

def getMachineByMac(mac):
  return Machine.query.filter_by(mac=mac).first()

def getMachineById(id):
  return Machine.query.filter_by(id=id).first()
  
def addMachine(userid, mac, mac_name):
  newMac = Machine(user_id = userid, mac =  mac, mac_name = mac_name)
  db.session.add(newMac)
  db.session.commit()
  return newMac
