from src.models.bot import BotScript, Bots, db
from src.utils import serializeList


def botByWorkspace(workspace_id):
  bot = Bots.query.filter_by(workspace_id=workspace_id).all()
  return Bots.serialize_list(bot)


def botByWorkspaceId(workspace_id, id):
  return Bots.query.filter_by(workspace_id=workspace_id, id=id).first()

def addBot(name, status, type, workspace):
  bot = Bots(name=name, status=status, type=type, workspace=workspace)
  db.session.add(bot)
  db.session.commit()
  return bot

def deleteBot(bot):
  db.session.delete(bot)
  db.session.commit()

def updateBot(bot, name):
  bot.name = name
  db.session.commit()

def saveBotScript(bot, script):
  bot.status = 'CONNECTED'
  botScript = BotScript(script = script, bot = bot)
  db.session.add(botScript)
  db.session.commit()
  return bot

def disconnectBot(bot):
  botScript = BotScript.query.filter_by(bot_id = bot.id)
  db.session.delete(botScript)
  bot.status = 'DISCONNECTED'
  db.session.save()

def botByWorkspaceMac(workspace_id):
  query = """
    SELECT
	b.name,
	b.status,
	b.updated_at,
	bs.script
FROM
	"rpa-test".bots as b
LEFT JOIN "rpa-test"."bot_script" as bs ON bs.bot_id = b.id
WHERE b.workspace_id = :w
  """
  data = db.session.execute(
      query,
      {'w': workspace_id}
  ).mappings().all()
  return serializeList(data)
