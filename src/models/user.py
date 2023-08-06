from src.models import *

class User(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  fullname = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.utc), onupdate=datetime.now(pytz.utc))
  workspaces = db.relationship('WorkspaceUsers', back_populates="user_data")
  def __repr__(self) -> str:
    return f'User>>> {self.fullname}'
  __table_args__ = {'schema': 'rpa-test'}

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password'}

  @staticmethod
  def serialize_list(l):
    return [m.as_dict() for m in l]

class TempUser(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  fullname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), nullable=False)
  otp = db.Column(db.String(6), nullable=False)
  verified = db.Column(db.Boolean, default=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

  __table_args__ = {'schema': 'rpa-test'}

class Machine(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = db.Column(UUID(as_uuid=True))
  mac = db.Column(db.String(20), unique=True, nullable=False)
  mac_name = db.Column(db.String(40), nullable=False)

  def __repr__(self) -> str:
    return f'Machine>>> {self.mac_name}'
  __table_args__ = {'schema': 'rpa-test'}
