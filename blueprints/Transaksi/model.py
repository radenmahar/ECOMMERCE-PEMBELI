from blueprints import db
from flask_restful import fields

class Transaksi(db.Model):
    __tablename__ = "transaksi"
    id_transaksi = db.Column(db.Integer, primary_key = True)
    id_pembeli = db.Column(db.Integer, nullable=False)
    id_barang = db.Column(db.Integer, nullable=False)
    nama_barang = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    nama_pembeli = db.Column(db.String(255), nullable=False)
    total_harga = db.Column(db.String(255), nullable=False)
    # total_quantity = db.Column(db.String(255), nullable=False)
    metode_transaksi = db.Column(db.String(255), nullable=False)

    response_fields = {
        'id_transaksi' : fields.Integer,
        'id_pembeli' : fields.Integer,
        'id_barang' : fields.Integer,
        'nama_barang' : fields.String,
        'username' : fields.String,
        'nama_pembeli' :fields.String,
        'total_harga' : fields.String,
        'metode_transaksi' : fields.String
    }

    def __init__(self, id_pembeli, id_barang, nama_barang, username, nama_pembeli, total_harga, metode_transaksi):
        # self.id_transaksi = id_transaksi
        self.id_pembeli = id_pembeli
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.username = username
        self.nama_pembeli = nama_pembeli
        self.total_harga = total_harga
        # self.total_quantity = total_quantity
        self.metode_transaksi = metode_transaksi
    
    def __repr__(self):
        return '<Transaksi %r>' % self.id_transaksi
