import os
import hashlib
import base64

import boto3

from flask import Flask, jsonify, request, make_response
app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    print("WARN: provisioning")
    client = boto3.client('dynamodb')

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/login", methods=["POST"])
def get_user():
  print("getting")
  username    = request.json.get('username')
  in_password = request.json.get('password')

  #if not [x for x in (username, password) if x is None]:
  if not username or not in_password:
    return jsonify({'error': 'Please provide username and password.'}), 400

  resp = client.get_item(
    TableName=USERS_TABLE,
    Key={
      'username': {'S': username}
    }
  )

  item = resp.get('Item')
  if not item:
    return jsonify({'error': 'Could not find user'}), 404

  password = item.get('password').get('S')
  salt = item.get('salt').get('S')

  salt = base64.b64decode(salt)

  in_password = hashlib.pbkdf2_hmac('sha512', bytes(in_password, encoding="ascii"), salt, 100000).hex()

  if not (password == in_password):
    return jsonify({'error': 'Could not authenticate'}), 401

  return jsonify({
    'username':     item.get('username').get('S'),
    'password':     item.get('password').get('S'),
    'salt':         item.get('salt').get('S'),
    'display_name': item.get('display_name').get('S'),
    'email':        item.get('email').get('S')
  })

@app.route("/register", methods=["POST"])
def create_user():
  print("posting")

  username     = request.json.get('username')
  password     = request.json.get('password')
  display_name = request.json.get('display_name')
  email        = request.json.get('email')

  #if not [x for x in (username, password, display_name, email) if x is None]:
  if not username or not password or not display_name or not email:
    return jsonify({'error': 'Please provide username, password, display_name, and email.'}), 400

  salt = os.urandom(32)
  
  password = hashlib.pbkdf2_hmac('sha512', bytes(password, encoding="ascii"), salt, 100000).hex()

  salt = str(base64.b64encode(salt), encoding="ascii")

  resp = client.put_item(
    TableName=USERS_TABLE,
    Item={
      'username':     {'S': username},
      'password':     {'S': password},
      'salt':         {'S': salt},
      'display_name': {'S': display_name},
      'email':        {'S': email}
    }
  )

  return jsonify({
    'username':     username,
    'password':     password,
    'salt':         salt,
    'display_name': display_name,
    'email':        email
  })

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
