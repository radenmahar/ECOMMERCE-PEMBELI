from blueprints import db
from flask_restful import fields

class Pembeli(db.Model):
    __tablename__ = "pembeli"
    id_pembeli = db.Column(db.Integer, primary_key = True)
    nama_pembeli = db.Column(db.String(255), nullable = False)
    user_name = db.Column(db.String(100), nullable = False)
    contact_pembeli = db.Column(db.String(100), nullable = False)
    email_pembeli = db.Column(db.String(30), nullable = False)
    password_pembeli = db.Column(db.String(30), nullable = False)
    status = db.Column(db.Boolean, nullable = False)

    response_fields = {
        'id_pembeli' : fields.Integer,
        'nama_pembeli' : fields.String,
        'user_name' : fields.String,
        'contact_pembeli' : fields.String,
        'email_pembeli' : fields.String,
        'password_pembeli' : fields.String,
        'status' : fields.Boolean

    }

    jwt_response_fields = {
        'id_pembeli' : fields.Integer,
        'nama_pembeli' : fields.String,
        'user_name' : fields.String,
        'contact_pembeli' : fields.String,
        'email_pembeli' : fields.String,
        'status' : fields.Boolean
    }

    def __init__(self, nama_pembeli, user_name, contact_pembeli, email_pembeli, password_pembeli, status):
        self.nama_pembeli = nama_pembeli
        self.user_name = user_name
        self.contact_pembeli = contact_pembeli
        self.email_pembeli = email_pembeli
        self.password_pembeli = password_pembeli
        self.status = status
    
    def __repr__(self):
        return '<User %r>' % self.id_pembeli

    @classmethod
    def is_exists(cls, data):

        all_data = cls.query.all()

        existing_nama_pembeli = [item.nama_pembeli for item in all_data]

        if data in existing_nama_pembeli:
            return True

        return False
