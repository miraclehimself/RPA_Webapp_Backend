from src.models import *
from src.models.user import User


class WorkspaceRole(enum.Enum):
  OWNER = "Owner"
  ADMIN = "Admin"
  MEMBER = "Member"

  def __str__(self):
    return self.value


class Workspace(db.Model):
  __tablename__ = 'workspace'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80), nullable=False)
  url = db.Column(db.String(80), unique=True, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace_users = db.relationship('WorkspaceUsers', back_populates="workspace")
  def __repr__(self) -> str:
    return f'Workspace>>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]

class WorkspaceUsers(db.Model):
  __tablename__ = 'workspace_users'
  id = db.Column(db.Integer, primary_key=True)
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id, ondelete='CASCADE'), nullable=False)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
      User.id, ondelete='CASCADE'), nullable=False)
  user_role = db.Column(db.Enum(WorkspaceRole), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace = db.relationship("Workspace", back_populates="workspace_users")
  user_data = db.relationship(User, back_populates="workspaces")
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]


class TWSU(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email = db.Column(db.String(120), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  role = db.Column(db.Enum(WorkspaceRole), nullable=False)
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id, ondelete='CASCADE'), nullable=False)
  __table_args__ = {'schema': 'rpa-test'}
