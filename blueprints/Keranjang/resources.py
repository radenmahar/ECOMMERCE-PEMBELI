import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Keranjang
from ..Barangs.model import Barang

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from blueprints import db, app, internal_required

bp_keranjang = Blueprint('keranjang', __name__)

api = Api(bp_keranjang)

class editKeranjang(Resource):
    def __init__(self):
        pass
    
    def options(self, id_keranjang=None):
        return {"status":"ok"},200

    def get(self, id_keranjang=None):
        qry = Keranjang.query.get(id_keranjang)
        if qry is not None:
          return marshal(qry, Keranjang.response_fields), 200, {'Content-Type' : 'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_barang', location = 'json', required=True)
        parser.add_argument('nama_barang', location = 'json', required=True)
        parser.add_argument('harga_barang', location = 'json', required=True)
        parser.add_argument('image_barang', location = 'json', required=True)
        args = parser.parse_args()

        claimJWt = get_jwt_claims()

        keranjang = Keranjang(claimJWt['id_pembeli'], args['id_barang'], args['nama_barang'], claimJWt['user_name'], claimJWt['nama_pembeli'], args['harga_barang'], args['image_barang'])
        db.session.add(keranjang)
        db.session.commit()


        app.logger.debug('DEBUG : %s', keranjang)

        return marshal(keranjang, Keranjang.response_fields), 200, {'Content-Type' : 'application/json'}
    
    @jwt_required
    @internal_required
    def delete(self, id_keranjang):
        qry = Keranjang.query.get(id_keranjang)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
    
    def patch(self):
        return "Not yet implemented", 501

class SemuaItemDiKeranjang(Resource):
    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', required = False, default = 1)
        parser.add_argument('rp', type = int, location = 'args', required = False, default = 25)
        parser.add_argument('id_pembeli', location = 'args', required=False)
        args = parser.parse_args()
        

        offset = args['p']*args['rp'] - args['rp']

        qry = Keranjang.query
        # claimJWt = get_jwt_claims()

        qry = qry.filter_by(id_pembeli=args['id_pembeli'])

        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []

        for row in qry:
            list_temp.append(marshal(row, Keranjang.response_fields))
        
        return list_temp, 200
    
api.add_resource(editKeranjang, '', '/<id_keranjang>')
api.add_resource(SemuaItemDiKeranjang, '/semuadikeranjang')
