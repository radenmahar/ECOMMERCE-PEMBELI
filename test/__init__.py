import pytest, json, logging
from flask import Flask, request
from blueprints.Pembeli.model import Pembeli
from blueprints.Keranjang.model import Keranjang
from blueprints import db, app 
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def reset_database():

    db.drop_all()
    db.create_all()

    pembeli = Pembeli("Kuntet", 'kunt', "082283511672","maharraden@gmail.com","agh765vx765", True)

    # barang = Barang("TOYOTA X8", "TOYOTA", "MAHAL", "7200000", "raden", "2017", "ohyeah")
    # create test non-admin user

    keranjang = Keranjang("1", "1", "toyota", "kun", "kuntet", "4500000", "faking")
    # save users to database
    db.session.add(pembeli)
    db.session.commit()

def create_token():
    token = cache.get('test-token')
    if token is None:
        data = {
            'email_pembeli' : 'maharraden@gmail.com',
            'password_pembeli' : 'agh765vx765'
        }
        # do request
        req = call_client(request)
        res = req.post('/login', data=json.dumps(data), content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token
