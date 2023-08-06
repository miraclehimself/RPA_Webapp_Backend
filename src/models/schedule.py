from src.models import *
from src.models.workspace import Workspace
from src.models.bot import Bots
from src.models.flows import Flows
class ScheduleType(enum.Enum):
  MINUTES = "Minutes"
  HOURLY = "Hourly"
  DAILY = "Daily"
  WEEKLY = "Weekly"
  MONTHLY = "Monthly"
  ADVANCE = "Advance"

  def __str__(self):
    return self.value
class Schedule(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80), nullable=False)
  robot_name = db.Column(db.String(80), nullable=False)
  robot_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
      Bots.id, ondelete='CASCADE'))
  flow_name = db.Column(db.String(80), nullable=False)
  flow_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
      Flows.id, ondelete='CASCADE'))
  flow_version = db.Column(db.Integer, nullable=False)
  schedule = db.Column(db.Enum(ScheduleType), nullable=False)
  cron_expression = db.Column(db.String(80), nullable=False)
  cron_command = db.Column(db.String(80), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id), nullable=False)
  workspace = db.relationship('Workspace', backref=backref(
      "schedules", cascade="all,delete"))
  def __repr__(self) -> str:
    return f'Schedule>>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]
