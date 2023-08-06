from datetime import timedelta
from operator import add
from flask import request
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from src.services.bot import addBot
from src.services.user import addUserWorkspace, deleteTempUser, getMachineByMac, userById, userByMail, addUser, addMachine, addTempUser, tempUser, validateTempUser
from src.services.workspace import addWorkspace, addWorkspaceUser, workspaceByName, workspaceByUrl, workspaceUserByEmail
from src.services.billing import addSubscription
from src.utils import getOTP, otpValid
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
from src.constants.app_constants import OTP_EXPIRATION_HRS

def userRegister():
  fullname = request.json['fullname']
  email = request.json['email']
  if not validators.email(email):
    return {'msg': 'Email not valid'}, HTTP_400_BAD_REQUEST
  if userByMail(email) is not None:
    return {'msg': 'Email has been used'}, HTTP_409_CONFLICT
  
  # otp = getOTP()
  otp = '00000'
  # To Do: Send email 
  try:
    user = addTempUser(fullname, otp, email)
    return {
      'msg': 'Email sent sucessfully',
      'data': {
        'temp_id': user.id
      }
    }, HTTP_201_CREATED

  except:
    return {'msg': 'An error occured'}, HTTP_500_INTERNAL_SERVER_ERROR


def verifyOTP():
  temp_id = request.json['temp_id']
  otp = request.json['otp']

  user = tempUser(temp_id)
  if user:
    if otp != user.otp:
      return {
        'msg': 'Incorrect OTP'
      }, HTTP_422_UNPROCESSABLE_ENTITY

    if not otpValid(user.created_at, OTP_EXPIRATION_HRS):
      return {
        'msg': 'OTP Expired'
      }, HTTP_422_UNPROCESSABLE_ENTITY
    validateTempUser(user)
    return {
      'msg': 'Verification Successful'
    }, HTTP_200_OK
  return {'msg': 'User not found'}, HTTP_404_NOT_FOUND

def setUp():
  # To do: remove unique value on workspace name
  temp_id = request.json['temp_id']
  password = request.json['password']
  robot_name = request.json['robot_name']
  workspace_name = request.json['workspace_name']
  workspace_url = request.json['workspace_url']

  if len(password) < 6:
    return {'msg': 'Password is too short'}, HTTP_400_BAD_REQUEST
  pass
  # if workspaceByName(workspace_name) is not None:
  #   return {'msg': 'Workspace name has been used'}, HTTP_409_CONFLICT

  if workspaceByUrl(workspace_url) is not None:
    return {'msg': 'Workspace url has been used'}, HTTP_409_CONFLICT

  temp_user = tempUser(temp_id)
  dt = timedelta(days=30)
  if temp_user and temp_user.verified:
    workspace = addWorkspace(name = workspace_name, url=workspace_url)
    user = addUser(temp_user.fullname,  generate_password_hash(password), temp_user.email)
    workspace_user = addWorkspaceUser(workspace, user, 'OWNER')
    user = addUserWorkspace(user, workspace_user)
    addBot(robot_name, 'DISCONNECTED', 'DEVELOPMENT', workspace)
    addSubscription('FREE', workspace)
    deleteTempUser(temp_user)
    userObj = {
      'userid': user.id,
      'workspaceid': workspace.id,
      'userrole': workspace_user.user_role
    }
    return {'msg': 'Setup Successful',
      'data': {
        'user': {
          'fullname': user.fullname,
          'email': user.email
        },
        'workspace': workspace.as_dict(),
        'refresh_token': create_refresh_token(identity=userObj),
        'access_token':  create_access_token(identity=userObj, expires_delta=dt)
    }
    }, HTTP_201_CREATED
  return {'msg': 'User data not found'}, HTTP_404_NOT_FOUND

def userLogin():
  email = request.json.get('email', '')
  password = request.json.get('password', '')
  workspace_url = request.json.get('workspace_url', '')

  workspace = workspaceByUrl(workspace_url)
  if not workspace:
    return {'msg': 'Invalid workspace url'}, HTTP_404_NOT_FOUND

  user = workspaceUserByEmail(workspace.id, email)
  dt = timedelta(days=30)
  if user:
    if check_password_hash(user['password'], password):
      userObj = {
        'userid': user['user_id'],
        'workspaceid': workspace.id,
        'userrole': user['user_role']
      }
      return {
        'msg': 'Setup Successful',
        'data': {
          'user': {
            'fullname': user['fullname'],
            'email': user['email']
          },
          'workspace': workspace.as_dict(),
          'refresh_token': create_refresh_token(identity=userObj),
          'access_token':  create_access_token(identity=userObj, expires_delta=dt)
        }
        }, HTTP_200_OK

  return {'msg': 'Incorrect username or password'}, HTTP_401_UNAUTHORIZED

def macLogin():
  email = request.json.get('email', '')
  password = request.json.get('password', '')
  workspace_url = request.json.get('workspace_url', '')
  mac_id = request.json['mac_id']
  workspace = workspaceByUrl(workspace_url)
  if not workspace:
    return {'msg': 'Invalid workspace url'}, HTTP_404_NOT_FOUND

  user = workspaceUserByEmail(workspace.id, email)
  dt = timedelta(days=30)
  if user:
    if check_password_hash(user['password'], password):
      userObj = {
          'userid': user['user_id'],
          'workspaceid': workspace.id,
          'userrole': user['user_role'],
          'macid': mac_id
      }
      return {
          'msg': 'Setup Successful',
          'data': {
              'user': {
                  'fullname': user['fullname'],
                  'email': user['email']
              },
              'workspace': workspace.as_dict(),
              'refresh_token': create_refresh_token(identity=userObj),
              'access_token':  create_access_token(identity=userObj, expires_delta=dt)
          }
      }, HTTP_200_OK

  return {'msg': 'Incorrect username or password'}, HTTP_401_UNAUTHORIZED

# def regMachine():
#   email = request.json['email']
#   password = request.json['password']
#   mac = request.json['mac']
#   mac_name = request.json['mac_name']
#   user = getUserByMail(email)
#   if user:
#     if check_password_hash(user.password, password):
#       machine = addMachine(user.id, mac, mac_name)
#       return {
#         'msg': 'Machine successfully added',
#         'data': {
#           'mac_id': machine.id,
#           'mac_name': mac_name
#         }
#       }, HTTP_201_CREATED
  
#   return {'msg': 'Incorrect username or password'}, HTTP_401_UNAUTHORIZED

# def authMachine():
#   mac = request.json.get('mac', '')
#   print(mac)
#   machine = getMachineByMac(mac)
#   print(machine)
#   if machine:
#     return {
#       'msg': 'Authentication Successful',
#       'data': {
#         'mac_id': machine.id,
#         'mac_name': machine.mac_name
#       }
#     }, HTTP_200_OK

#   return {'msg': 'Machine not recognise'}, HTTP_401_UNAUTHORIZED
