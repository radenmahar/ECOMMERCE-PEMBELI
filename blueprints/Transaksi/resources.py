import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Transaksi
from ..Barangs.model import Barang

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from blueprints import db, app, internal_required

bp_transaksi = Blueprint('transaksi', __name__)

api = Api(bp_transaksi)

class editTransaksi(Resource):
    def __init__(self):
        pass
    
    def options(self, id_transaksi=None):
        return {"status":"ok"},200

    def get(self, id_transaksi):
        qry = Transaksi.query.get(id_transaksi)
        if qry is not None:
          return marshal(qry, Transaksi.response_fields), 200, {'Content-Type' : 'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('id_pembeli', location='json', required=True)
        parser.add_argument('id_barang', location = 'json', required=True)
        parser.add_argument('nama_barang', location = 'json', required=True)
        # parser.add_argument('username', location = 'json', required=True)
        # parser.add_argument('nama_pembeli', location = 'json', required=True)
        parser.add_argument('total_harga', location = 'json', required=True)
        parser.add_argument('metode_transaksi', location = 'json', required=True)
        args = parser.parse_args()

        claimJWt = get_jwt_claims()

        transaksi = Transaksi(claimJWt['id_pembeli'], args['id_barang'], args['nama_barang'], claimJWt['user_name'], claimJWt['nama_pembeli'], args['total_harga'], args['metode_transaksi'])
        db.session.add(transaksi)
        db.session.commit()

        app.logger.debug('DEBUG : %s', transaksi)

        return marshal(transaksi, Transaksi.response_fields), 200, {'Content-Type' : 'application/json'}

    @jwt_required
    @internal_required
    def put(self, id_transaksi):
        parser = reqparse.RequestParser()
        # parser.add_argument('id_pembeli', location='json', required=False)
        # parser.add_argument('id_barang', location = 'json', required=False)
        # parser.add_argument('nama_barang', locaton = 'json', require=False)
        # parser.add_argument('username', location = 'json', required=False)
        # parser.add_argument('nama_pembeli', location = 'json', required=False)
        # parser.add_argument('total_harga', location = 'json', required=False)
        # parser.add_argument('total_quantity', location = 'json', required=False)
        parser.add_argument('metode_transaksi', location = 'json', required=False)
        args = parser.parse_args()

        qry = Transaksi.query.get(id_transaksi)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        # if args['id_pembeli'] is not None:
        #     qry.id_pembeli = args['id_pembeli']
        # if args['id_barang'] is not None:
        #     qry.id_barang = args['id_barang']
        # if args['nama_barang'] is not None:
        #     qry.nama_barang = args['nama_barang']
        # if args['username'] is not None:
        #     qry.username = args['username']
        # if args['nama_pembeli'] is not None:
        #     qry.nama_pembeli = args['nama_pembeli']
        # if args['total_harga'] is not None:
        #     qry.total_harga = args['total_harga']
        # if args['total_quantity'] is not None:
        #     qry.total_quantity = args['total_quantity']
        if args['metode_transaksi'] != "":
            qry.metode_transaksi = args['metode_transaksi']
        db.session.commit()

        return marshal(qry, Transaksi.response_fields), 200
    
    @jwt_required
    @internal_required
    def delete(self, id_transaksi):
        qry = Transaksi.query.get(id_transaksi)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
    
    def patch(self):
        return "Not yet implemented", 501

class SemuaTransaksi(Resource):
    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        parser.add_argument('id_barang', location = 'body', required=False)
        args = parser.parse_args()
        

        offset = args['p']*args['rp'] - args['rp']

        qry = Pembeli.query

        if args['id_barang'] is not None:
            qry = qry.filter_by(id_barang=args['id_barang'])

        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Transaksi.response_fields))
        
        return list_temp, 200
    
api.add_resource(editTransaksi, '', '/<id_transaksi>')
api.add_resource(SemuaTransaksi, '/semuatransaksi')
