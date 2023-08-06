from src.models import *


class FunctionGroup(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  group_name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=True, nullable=False)


  def __repr__(self) -> str:
    return f'Function Group>>> {self.username}'
  __table_args__ = {'schema': 'rpa-test'}


class Functions(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  group_id = db.Column(UUID(as_uuid=True))
  function_name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=True, nullable=False)
  input = db.Column(ARRAY(JSON))
  output = db.Column(ARRAY(JSON))
  options = db.Column(ARRAY(JSON))

  def __repr__(self) -> str:
    return f'Function>>> {self.username}'
  __table_args__ = {'schema': 'rpa-test'}
