from src.models import *
from src.models.workspace import Workspace
from src.models.user import User

class SharedType(enum.Enum):
  PRIVATE = 'Private'
  PUBLIC = 'Public'
  WORKSPACE = 'Workspace'

  def __str__(self):
    return self.value



class Flows(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80), nullable=False)
  created_by = db.Column(UUID(as_uuid=True),db.ForeignKey(User.id), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id), nullable=False)
  shared_type = db.Column(db.Enum(SharedType), nullable=False)
  shared_with = db.Column(ARRAY(UUID(as_uuid=True)))
  versions = db.Column(db.Integer, nullable=False)
  workspace = db.relationship('Workspace', backref=backref(
      "flows", cascade="all,delete"))
  def __repr__(self) -> str:
    return f'Flow>>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns }

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]


class FlowData(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80))
  description = db.Column(db.String(80))
  flow_name = db.Column(db.String(80), nullable=False)
  flow_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
      Flows.id, ondelete='CASCADE'), nullable=False)
  nodes = db.Column(ARRAY(JSON))
  link = db.Column(ARRAY(JSON))
  flow = db.relationship(Flows, backref=backref(
      "flow_data", cascade="all,delete"))
  version = db.Column(db.Integer, nullable=False)
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]
