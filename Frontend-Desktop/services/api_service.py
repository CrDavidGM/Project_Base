import requests

#URL = http://127.0.0.1:5000/usuarios
class ApiService:
    def get_data(self,letra=""):
        response = requests.get(f"http://127.0.0.1:5000/usuarios?letra={letra}")
        if response.status_code == 200:
            return response.json()
        else:
            return None

    
    def add_user(self,new_user):
        requests.post("http://127.0.0.1:5000/usuarios",json=new_user)


    def update_user(self,user_id,updated_user):
        requests.put(f"http://127.0.0.1:5000/usuarios/{user_id}",json=updated_user)


    def delete_user(self,user_id):
        response = requests.delete(f'http://127.0.0.1:5000/usuarios/{user_id}')
        if response.status_code == 200:
            print(f"Usuario {user_id} eliminado")
        else:
            print(f"Error al eliminar usuario {user_id}: {response.status_code}")