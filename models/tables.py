from database.db import db
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def check_password(self, password_attempt):
        return self.password == password_attempt

    def __repr__(self):
        return '<Admin %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class SorteosGuardados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(100), nullable=False)
    resultados = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<SorteosGuardados %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "resultados": self.resultados,
        }

