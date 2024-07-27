from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    grado = db.Column(db.String(100), nullable=False)
    seccion = db.Column(db.String(100), nullable=False)