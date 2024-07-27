import requests

# URL del endpoint para agregar un usuario
url = 'http://127.0.0.1:5000/usuarios'

# Datos del nuevo usuario
nuevo_usuario = {
    'nombre': 'Kevin',
    'correo': 'Kevin@example.com'
}

# Enviar la solicitud POST
response = requests.post(url, json=nuevo_usuario)

# Imprimir la respuesta del servidor
print(response.status_code)
print(response.json())