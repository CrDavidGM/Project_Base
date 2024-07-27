from app import app, db
from flask import jsonify, request
from app.models import Usuario

@app.route('/')
def home():
    return "Home"

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{"nombre": u.nombre, "correo": u.correo} for u in usuarios])

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    nuevo_usuario = Usuario(nombre=data['nombre'], correo=data['correo'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario añadido"}), 201