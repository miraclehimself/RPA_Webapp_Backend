
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.controllers.bot import addBots, botDisconnect, botMac, delBot, getBots, patchBot
bot = Blueprint("bots", __name__, url_prefix="/bots")


@bot.get('/')
@jwt_required()
# @swag_from('../docs/bots/bots.yaml')
def bots():
  identity = get_jwt_identity()
  return getBots(identity['workspaceid'])


@bot.get('/<string:mac_id>')
@jwt_required()
# @swag_from('../docs/bots/bots.yaml')
def mac_bots(mac_id):
  identity = get_jwt_identity()
  return botMac(mac_id, identity)

@bot.post('/')
@jwt_required()
def add_bot():
  identity = get_jwt_identity()
  return addBots(identity)


@bot.delete('/<uuid:bot_id>')
@jwt_required()
def delete_bot(bot_id):
  identity = get_jwt_identity()
  return delBot(bot_id, identity)


@bot.patch('/<uuid:bot_id>')
@jwt_required()
def edit_bot(bot_id):
  identity = get_jwt_identity()
  return patchBot(bot_id, identity)


@bot.post('/<uuid:bot_id>')
@jwt_required()
def disconnect_bot(bot_id):
  identity = get_jwt_identity()
  return botDisconnect(bot_id, identity)
