from src.models import *
from src.models.workspace import Workspace

class BotStatus(enum.Enum):
  DISCONNECTED = "Disconnected"
  CONNECTED = "Connected"

  def __str__(self):
    return self.value


class BotType(enum.Enum):
  DEVELOPMENT = "Development"
  PRODUCTION = "Production"
  ON_DEMAND = "On Demand"

  def __str__(self):
    return self.value



class Bots(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String(80), nullable=False)
  token = db.Column(db.String(80))
  status = db.Column(db.Enum(BotStatus), nullable=False)
  type = db.Column(db.Enum(BotType), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace = db.relationship('Workspace', backref=backref(
      "bots", cascade="all,delete"))
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id), nullable=False)
  def __repr__(self) -> str:
    return f'Bot>>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]

class BotScript(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  script = db.Column(db.Text())
  bot_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
      Bots.id, ondelete='CASCADE'), nullable=False)
  bot = db.relationship(Bots, backref=backref("flow_data", uselist=False, cascade="all,delete"))
  __table_args__ = {'schema': 'rpa-test'}
