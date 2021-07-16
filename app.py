from typing import Optional

import os
import hashlib
import base64

import boto3

from fastapi import FastAPI, HTTPException, status 
from pydantic import BaseModel, EmailStr

USERS_TABLE: str = os.environ['USERS_TABLE']
IS_OFFLINE: str = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
  client = boto3.client(
    'dynamodb',
    region_name='localhost',
    endpoint_url='http://localhost:8000'
  )
else:
  client = boto3.client('dynamodb')

# Requests
class LoginRequest(BaseModel):
  username: EmailStr
  password: str

class RegistrationRequest(BaseModel):
  username:     EmailStr
  password:     str
  display_name: str

# Responses
class UserInfo(BaseModel):
  username:     EmailStr
  password:     str
  salt:         str
  display_name: str

app = FastAPI()

@app.post("/login", response_model=UserInfo, status_code=status.HTTP_200_OK)
def get_account(login_request: LoginRequest):
  db_get = client.get_item(
    TableName=USERS_TABLE,
    Key={
      'username': {'S': login_request.username}
    }
  )

  item = db_get.get('Item')

  if not item:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

  password = item.get('password').get('S')
  request_salt = item.get('salt').get('S')

  request_salt = base64.b64decode(request_salt)

  request_hash = hashlib.pbkdf2_hmac('sha512', bytes(login_request.password, encoding="ascii"), request_salt, 100000).hex()

  if not (password == request_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate.")

  return {
    'username':     item.get('username').get('S'),
    'password':     item.get('password').get('S'),
    'salt':         item.get('salt').get('S'),
    'display_name': item.get('display_name').get('S'),
    'email':        item.get('email').get('S')
  }

@app.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
def create_user(regis_request: RegistrationRequest):
  request_salt = os.urandom(32)
  
  request_hash = hashlib.pbkdf2_hmac('sha512', bytes(regis_request.password, encoding="ascii"), request_salt, 100000).hex()

  request_salt = str(base64.b64encode(request_salt), encoding="ascii")

  resp = client.put_item(
    TableName=USERS_TABLE,
    Item={
      'username':     {'S': regis_request.username},
      'password':     {'S': request_hash},
      'salt':         {'S': request_salt},
      'display_name': {'S': regis_request.display_name},
    }
  )

  return {
    'username':     regis_request.username,
    'password':     request_hash,
    'salt':         request_salt,
    'display_name': regis_request.display_name,
  }
