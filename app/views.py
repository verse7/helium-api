import os
import jwt
from functools import wraps
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app import app, db, csrf
from app.forms import RegisterForm, LoginForm, PostForm
from app.models import User, Post

###
# Utility functions
###

def auth_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': r'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    return f(*args, **kwargs)

  return decorated

def get_form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

###
# api endpoints
###

@app.route('/users', methods=['POST'])
@csrf.exempt
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        trn = form.trn.data
        username = form.username.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        
        user = User(trn, username, password, firstname, lastname, email, phone, 
                    address)
        
        db.session.add(user)
        db.session.commit()
 
        response = { 'message': 'User registered successfully!'}, 201
    else:
        response = { 'errors': get_form_errors(form) }, 400
        
    return jsonify(response[0]), response[1]
    

@app.route('/users/login', methods=['POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # find a user with the same username and try to match the passwords
        user = User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode({'id': user.id, 'username': username}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
                response = {'token': token, 'message': 'User successfully logged in!'}, 200
            else:
                response = {'errors': ['Incorrect username or password!']}, 400
        else:
            response = {'errors': ['Incorrect username or password!']}, 400
    else:
        response = {'errors': get_form_errors(form)}, 400
    
    return jsonify(response[0]), response[1]

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
