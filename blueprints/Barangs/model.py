from blueprints import db
from flask_restful import fields

class Barang(db.Model):
    __tablename__ = 'barang'
    barang_id = db.Column(db.Integer, primary_key = True)
    nama_barang = db.Column(db.String(255), nullable = False)
    tipe_barang = db.Column(db.String(255), nullable = False)
    deskripsi_barang = db.Column(db.String(1000), nullable = False)
    harga_barang = db.Column(db.String(255), nullable = False)
    username_pelapak = db.Column(db.String(255), nullable = False)
    tahun_barang = db.Column(db.String(255), nullable = True)
    image_barang = db.Column(db.String(255), nullable = False)

    response_fields = {
        'barang_id' : fields.Integer,
        'nama_barang' : fields.String,
        'tipe_barang' : fields.String,
        'deskripsi_barang' : fields.String,
        'harga_barang' : fields.String,
        'username_pelapak' : fields.String,
        'tahun_barang' : fields.String,
        'image_barang' : fields.String
    }

    def __init__(self, nama_barang, tipe_barang, deskripsi_barang, harga_barang, jumlah_barang, username_pelapak, tahun_barang, image_barang):
        self.nama_barang = nama_barang
        self.tipe_barang = tipe_barang
        self.deskripsi_barang = deskripsi_barang
        self.harga_barang = harga_barang
        self.username_pelapak = username_pelapak
        self.tahun_barang = tahun_barang
        self.image_barang = image_barang
    
    def __repr__(self):
        return '<Barang %r>' % self.barang_id