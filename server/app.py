#!/usr/bin/env python3

import os
from flask import Flask, request, make_response, jsonify, session, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, IntegerField
from sqlalchemy.exc import IntegrityError
from models import db, User, Address
from flask_cors import CORS
from flask_restful import reqparse
import jwt
from datetime import datetime, timedelta
from functools import wraps
# from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'G\xb2\xa4\xff\xc6~bM\xb9\x8c\xb3M'

db.init_app(app)
bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
migrate = Migrate(app, db)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 401
        return func(*args, **kwargs)

    return decorated



@app.route('/signup', methods=['POST'])
def signup():
    # Parse incoming JSON data
    data = request.get_json()

    # Validate incoming data
    required_fields = ['username', 'email', 'password', 'firstname', 'lastname']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Username or email already exists. Please choose a different one.'}), 400

    # Create a new user instance
    new_user = User(
        username=data['username'],
        email=data['email'],
        firstname=data['firstname'],
        lastname=data['lastname']
    )
    new_user.password_hash = data['password']

    # Add the new user to the database
    db.session.add(new_user)

    try:
        # Commit the session to persist the changes
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 200
    except:
        # Rollback the session in case of an error
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'error': 'Missing username or password'}, 400

    # Replace this logic with your actual authentication mechanism (e.g., querying the database)
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user._password_hash, password):
        token = jwt.encode({
            'user': username,
            'exp': datetime.utcnow() + timedelta(seconds=120)
        },
        app.config['SECRET_KEY'])

        return {'token': token}

    else:
        return {'error': 'Invalid username or password'}, 401
    
@app.route('/logout', methods=["DELETE"])
def logout():
    session['user_id'] = None
    return {'message': 'Logout successful'}, 200

@app.route('/public')
def public():
    return 'for public'


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard'

@app.route('/checksession', methods=["GET"])
def checksession():
    
    user_id = session['user_id']
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return user.to_dict(), 200
    
    return {}, 401 

@app.route('/address', methods=['POST'])
def create_address():
    data = request.get_json()

    # Validate incoming data
    required_fields = ['user_id', 'street', 'city', 'state', 'zip_code', 'country']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_address = Address(
        user_id=data['user_id'],
        street=data['street'],
        city=data['city'],
        state=data['state'],
        zip_code=data['zip_code'],
        country=data['country']
    )

    db.session.add(new_address)
    db.session.commit()
    
    return jsonify({'message': 'Address created successfully', 'address': new_address.id}), 201


if  __name__ == '__main__':
    app.run(port=5555, debug=True)