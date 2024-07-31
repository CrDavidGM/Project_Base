import requests
import tkinter as tk
# URL del endpoint para agregar un usuario

class interfaz():
    
    def __init__(self) -> None:
        self.url = 'http://127.0.0.1:5000/usuarios'
        root = tk.Tk()

        label_1 = tk.Label(root,text="Nombre")
        label_1.pack()

        input_1 = tk.Entry(root)
        input_1.pack()

        label_2 = tk.Label(root,text="Correo")
        label_2.pack()

        input_2 = tk.Entry(root)
        input_2.pack()

        boton = tk.Button(root,text="Enviar datos",command=lambda: self.write_new_user(input_1.get(),input_2.get()))
        boton.pack()

        self.label_3 = tk.Label(root)
        self.label_3.pack()

        button_2 = tk.Button(root,text="Usuarios",command=self.get_users)
        button_2.pack()

        root.mainloop()


    def get_users(self):
        response = requests.get(self.url)
        self.label_3.config(text=response.json())


    def write_new_user(self,nombre,correo):
        # Datos del nuevo usuario
        nuevo_usuario = {
            'nombre': nombre,
            'correo': correo
        }

        # Enviar la solicitud POST
        response = requests.post(self.url, json=nuevo_usuario)
        return response
    

if __name__ == "__main__":

    inter = interfaz()