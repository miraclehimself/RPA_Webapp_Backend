from src.models import *
from src.models.workspace import Workspace
from src.models.bot import Bots
from src.models.flows import Flows
# To do: Dynamic enum for trigger_item

class TriggerType(enum.Enum):
  FILE_SYSTEM = "File System"
  EMAIL = "Email"

  def __str__(self):
    return self.value
class Trigger(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(120), nullable=False)
  robot_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Bots.id))
  robot = db.relationship('Bots', backref=backref(
      "triggers", cascade="all,delete"))
  flow_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Flows.id))
  flow_version = db.Column(db.Integer, nullable=False)
  flow = db.relationship('Flows', backref=backref(
      "triggers", cascade="all,delete"))
  trigger_type = db.Column(db.Enum(TriggerType), nullable=False)
  trigger_item = db.Column(db.String(80), nullable=False)
  trigger_properties = db.Column(JSON(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id), nullable=False)
  workspace = db.relationship('Workspace', backref=backref(
      "triggers", cascade="all,delete"))
  def __repr__(self) -> str:
    return f'Trigger>>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]
