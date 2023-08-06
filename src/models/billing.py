from src.models import *
from src.models.workspace import Workspace

class BillingType(enum.Enum):
  FREE = "Free"
  BASIC = "Basic"
  PREMIUM = "Prenium"

  def __str__(self):
    return self.value
class PeriodType(enum.Enum):
  MONTHLY = 'Monthly'
  YEARLY = 'Yearly'

  def __str__(self):
    return self.value
class StatusType(enum.Enum):
  ACTIVE = 'Active'
  INACTIVE = 'Inactive'

  def __str__(self):
    return self.value
    
class Subscriptions(db.Model):
  __tablename__ = 'subscriptions'
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = db.Column(db.Enum(BillingType), nullable=False)
  user_limit = db.Column(db.Integer, nullable=False)
  prod_robot = db.Column(db.Integer, nullable=False)
  dev_robot = db.Column(db.Integer, nullable=False)
  on_demand_robot = db.Column(db.Integer, nullable=False)
  period = db.Column(db.Enum(PeriodType), nullable=False)
  next_pay_date = db.Column(db.DateTime)
  amount = db.Column(db.Numeric(10, 2))
  status = db.Column(db.Enum(StatusType), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(
      pytz.utc), onupdate=datetime.now(pytz.utc))
  workspace_id = db.Column(
      UUID(as_uuid=True), db.ForeignKey(Workspace.id), nullable=False)
  workspace = db.relationship('Workspace', backref=backref(
      "subscription", cascade="all,delete"), uselist=False)
  def __repr__(self) -> str:
    return f'Subscription>> {self.name}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]
