from blueprints import db
from flask_restful import fields

class Keranjang(db.Model):
    __tablename__ = "keranjang"
    id_keranjang = db.Column(db.Integer, primary_key = True)
    id_pembeli = db.Column(db.Integer, nullable=False)
    id_barang = db.Column(db.Integer, nullable=False)
    nama_barang = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    nama_pembeli = db.Column(db.String(255), nullable=False)
    harga_barang = db.Column(db.String(255), nullable=False)
    image_barang = db.Column(db.String(255), nullable = False)

    response_fields = {
        'id_keranjang' : fields.Integer,
        'id_pembeli' : fields.Integer,
        'id_barang' : fields.Integer,
        'nama_barang' : fields.String,
        'username' : fields.String,
        'nama_pembeli' :fields.String,
        'harga_barang' : fields.String,
        'image_barang': fields.String
    }

    def __init__(self, id_pembeli, id_barang, nama_barang, username, nama_pembeli, harga_barang, image_barang):
        self.id_pembeli = id_pembeli
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.username = username
        self.nama_pembeli = nama_pembeli
        self.harga_barang = harga_barang
        self.image_barang = image_barang
    
    def __repr__(self):
        return '<Keranjang %r>' % self.id_keranjang
