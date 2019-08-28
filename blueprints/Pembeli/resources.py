import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Pembeli

from flask_jwt_extended import jwt_required
from blueprints import db, app, internal_required

bp_pembeli = Blueprint('pembeli', __name__)

api = Api(bp_pembeli)

class editPembeli(Resource):
    def __init__(self):
        pass
    
    def options(self):
        return {"status":"ok"},200
    
    @jwt_required
    @internal_required
    def get(self, pembeli_id):
        qry = Pembeli.query.get(pembeli_id)
        if qry is not None:
            return marshal(qry, Pembeli.response_fields), 200, {'Content-Type' : 'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pembeli', location ='json', required=True)
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('contact_pembeli', location = 'json', required=True)
        parser.add_argument('email_pembeli', location = 'json', required=True)
        parser.add_argument('password_pembeli', location = 'json', required=True)
        args = parser.parse_args()

        status = True
        pembeli = Pembeli(args['nama_pembeli'], args['user_name'], args['contact_pembeli'], args['email_pembeli'], args['password_pembeli'], status)
        db.session.add(pembeli)
        db.session.commit()

        app.logger.debug('DEBUG : %s', pembeli)

        return marshal(pembeli, Pembeli.response_fields), 200, {'Content-Type' : 'application/json'}
    
    @jwt_required
    @internal_required
    def put(self, pembeli_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pembeli', location ='json', required=False)
        parser.add_argument('user_name', location='json', required=False)
        parser.add_argument('contact_pembeli', location = 'json', required=False)
        parser.add_argument('email_pembeli', locaton = 'json', require=False)
        parser.add_argument('password_pembeli', location = 'json', required=False)
        args = parser.parse_args()

        qry = Pembeli.query.get(pembeli_id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        if args['nama_pembeli'] is not None:
            qry.nama_pembeli = args['nama_pembeli']
        if args['user_name'] is not None:
            qry.user_name = args['user_name']
        if args['contact_pembeli'] is not None:
            qry.contact_pembeli = args['contact_pembeli']
        if args['email_pembeli'] is not None:
            qry.email_pembeli = args['email_pembeli']
        if args['password_pembeli'] is not None:
            qry.password_pembeli = args['password_pembeli']
        db.session.commit()

        return marshal(qry, Pembeli.response_fields), 200
    
    def delete(self, pembeli_id):
        qry = Pembeli.query.get(pembeli_id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200

    def patch(self):
        return "Not yet implemented", 501

class SemuaPembeli(Resource):
    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        parser.add_argument('user_name', location = 'body')
        args = parser.parse_args()
        

        offset = args['p']*args['rp'] - args['rp']

        qry = Pembeli.query

        if args['user_name'] is not None:
            qry = qry.filter_by(user_name=args['user_name'])

        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Pembeli.response_fields))
        
        return list_temp, 200
    
api.add_resource(editPembeli, '', '/<pembeli_id>')
api.add_resource(SemuaPembeli, '', '/listpembeli')

