import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import Barang
from flask_jwt_extended import jwt_required

from . import *
from blueprints import db, app, internal_required
from mailjet_rest import Client
import os


bp_barang = Blueprint('barang', __name__)

api = Api(bp_barang)

class BarangById(Resource):
    def __init__(self):
        pass
    
    def options(self, barang_id=None):
        return {"status":"ok"},200
    
    @jwt_required
    @internal_required
    def get(self, barang_id):
        Qry = Barang.query.get(barang_id)
        if Qry is not None:
            return marshal(Qry, Barang.response_fields), 200, {'Content-Type' : 'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    def delete(self, barang_id):
        qry = Barang.query.get(barang_id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()
    
    def patch(self):
        return "Not yet implemented", 501

class SearchBarang(Resource):
    def __init__(self):
        pass

    def options(self, barang_id=None):
        return {"status":"ok"},200
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        parser.add_argument('katakunci', location = 'args', required = False)
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Barang.query

        print(qry)

        qry= qry.limit(args['rp']).offset(offset).all()
        list_temp = []

        for row in qry:
            #cek apakah barang yang dicari ada di nama barang atau tipe barang
            if args['katakunci'] != "" or args['katakunci'] is not None:
                if args['katakunci'].lower() in row.nama_barang.lower() or args['katakunci'].lower() in row.tipe_barang.lower():
                    print("data ku",marshal(row, Barang.response_fields))
                    list_temp.append(marshal(row, Barang.response_fields))
        
        return list_temp, 200

class SemuaBarang(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Barang.query

        print(qry)

        qry= qry.limit(args['rp']).offset(offset).all()
        list_temp = []

        for row in qry:
            print("data ku",marshal(row, Barang.response_fields))
            list_temp.append(marshal(row, Barang.response_fields))
        
        return list_temp, 200

class Cobanembak(Resource):
    def __init__(self):
        pass
    
    def options(self, barang_id=None):
        return {"status":"ok"},200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('namaPembeli', location = 'json', required=False)
        parser.add_argument('emailtujuan', location = 'json', required=False)
        parser.add_argument('Barang', location = 'json', required=False)
        parser.add_argument('ID', location = 'json', required=False)
        parser.add_argument('alamat', location = 'json', required=False)
        parser.add_argument('total', location = 'json', required=False)
        args = parser.parse_args()

        api_key = '7d927645648521586a2e8def9ed3c828'
        api_secret = '325f24a29a6132ba6b1baf30c6115e00'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
                {
                    "From": {
                        "Email": "radenmaharjo@gmail.com",
                        "Name": "Beliaja"
                    },
                            "To": [
                        {
                            "Email": args['emailtujuan'],
                            "Name": "passenger 1"
                        }
                    ],
                    "TemplateID": 974381,
                    "TemplateLanguage": True,
                    "Subject": "Transaksi BeliAja",
                    "Variables": {
            "namaPembeli": args['namaPembeli'],
            "Barang": args['Barang'],
            "ID": args['ID'],
            "alamat": args['alamat'],
            "total": args['total']
        }
                }
            ]
        }
        
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        return result.json(), 200

api.add_resource(BarangById, '', '/<barang_id>')
api.add_resource(SearchBarang, '/search')
api.add_resource(SemuaBarang, '/semuabarang')
api.add_resource(Cobanembak, '/nembak')        



        

