from app import app, db
from flask import jsonify, request
from app.models import Usuario

@app.route('/')
def home():
    return "Home"

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    letra = request.args.get('letra', '').lower()  # Obtiene la letra del parámetro de consulta y la convierte a minúsculas
    if letra:
        usuarios = Usuario.query.filter(Usuario.nombre.ilike(f'{letra}%')).all()
    else:
        usuarios = Usuario.query.all()
    return jsonify([{"id": u.id, "nombre": u.nombre, "correo": u.correo} for u in usuarios])


@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    nuevo_usuario = Usuario(nombre=data['nombre'], correo=data['correo'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario añadido"}), 201


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200


@app.route('/usuarios/<int:id>', methods=['PUT'])
def edit_usuario(id):
    data = request.json  # Obtiene los datos del cuerpo de la solicitud en formato JSON
    
    # Buscar el usuario por id
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Validar y actualizar los campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'correo' in data:
        usuario.correo = data['correo']

    # Guardar los cambios en la base de datos
    db.session.commit()
    return jsonify({"message": "Usuario actualizado", "usuario": {"id": usuario.id, "nombre": usuario.nombre, "correo": usuario.correo}})