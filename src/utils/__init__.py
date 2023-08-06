from flask.json import JSONEncoder
import datetime
import random
from uuid import UUID

class CustomJSONEncoder(JSONEncoder):
  "Add support for serializing timedeltas"

  def default(self, o):
    if type(o) == datetime.timedelta:
      return str(o)
    elif type(o) == datetime.datetime:
      return o.isoformat()
    elif type(o) == UUID:
      return str(o)
    elif type(o) == str or type(o) == bool or type(o) == int or type(o) == float:
      return super().default(o)
    else:
      return str(o)



def getOTP(length = 5):
  return ''.join([str(x) for x in random.sample(range(0, 9), length)])

def otpValid(otptime, validPeriod):
  now = datetime.datetime.now()
  timeDiff = now - otptime
  hrs = timeDiff/3600
  return hrs < datetime.timedelta(hours = validPeriod)

def serializeData(data):
  if not data:
    return data
  d = {}
  for column, value in data.items():
    # build up the dictionary
    d = {**d, **{column: value}}

  return d

def serializeList(data):
  d, a = {}, []

  for rowproxy in data:
    # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
    for column, value in rowproxy.items():
      # build up the dictionary
      d = {**d, **{column: value}}
    a.append(d)

  return a
