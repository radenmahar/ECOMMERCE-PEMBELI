from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
import requests
import os
import config
from werkzeug.contrib.cache import SimpleCache
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e:
    raise e

cache = SimpleCache()

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

app.config['JWT_SECRET_KEY'] = 'Skjakdjladd668adkka'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=5)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

#jwt custom decorator admin
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status':'forbidden', 'message':'internal only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception:
        requestData = request.args.to_dict()
    
    if response.status_code > 200:
        app.logger.error("REQUEST_LOG\t%s", 
            json.dumps({
            'method': request.method, 
            'code': response.status,
            'uri': request.full_path, 
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))}))
        return response
    else:
        app.logger.warning("REQUEST_LOG\t%s", 
            json.dumps({
            'method': request.method, 
            'code': response.status,
            'uri': request.full_path, 
            'request': requestData, 
            'response': json.loads(response.data.decode('utf-8'))}))
        return response



from blueprints.Pembeli.resources import bp_pembeli
from blueprints.Login import bp_login
from blueprints.Barangs.resources import bp_barang
from blueprints.Keranjang.resources import bp_keranjang


app.register_blueprint(bp_pembeli, url_prefix='/pembeli')
app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_barang, url_prefix='/barang')
app.register_blueprint(bp_keranjang, url_prefix='/keranjang')
db.create_all()
