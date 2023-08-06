
from flask import Blueprint

from flasgger import swag_from
from src.controllers.auth import macLogin, userRegister, verifyOTP, setUp, userLogin
auth = Blueprint("auth", __name__, url_prefix="/auth")

# @user.post('/register')
# @swag_from('../docs/user/register.yaml')
# def register():
#   return userRegister()


# @user.post('/login')
# @swag_from('../docs/user/login.yaml')
# def login():
#   return userLogin()

# @user.post('/machine/register')
# def registerMachine():
#   return regMachine()

# @user.post('/machine/login')
# def machinLogin():
#   return authMachine()

@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():
  return userRegister()


@auth.post('/verifyotp')
@swag_from('../docs/auth/verifyotp.yaml')
def verifyotp():
  return verifyOTP()


@auth.post('/setup')
@swag_from('../docs/auth/register.yaml')
def setup():
  return setUp()


@auth.post('/login')
@swag_from('../docs/auth/login.yaml')
def login():
  return userLogin()


@auth.post('/login/machine')
@swag_from('../docs/auth/login.yaml')
def mac_login():
  return macLogin()
