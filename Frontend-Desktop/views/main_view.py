import tkinter as tk
from tkinter import ttk
import json
from typing import List


class UserCard(tk.Frame):

    user_card_list:List["UserCard"] = []

    #main_instance = es la instancia principal, en este caso la vista principal,
    #para obtener los datos necesarios.
    def __init__(self, master=None, main_instance:"MainView"=None,user_id= None,name=None, mail=None, delete_callback=None, update_callback=None,**kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.name = name
        self.mail = mail
        self.delete_callback = delete_callback
        self.update_callback = update_callback
        self.user_card_list.append(self)
        self.is_editing = False
        self.main_instance = main_instance
        self.create_card()


    def create_card(self):
        label_name = tk.Label(self, text=self.name)
        label_name.grid(row=0, column=0, sticky="wens")

        label_mail = tk.Label(self, text=self.mail)
        label_mail.grid(row=1, column=0, sticky="wens")

        self.edit_button = tk.Button(self, text="Editar",command=self.update_user)
        self.edit_button.grid(row=0, column=1, sticky="wens")

        delete_button = tk.Button(self, text="Eliminar",command=self.delete_user)
        delete_button.grid(row=1, column=1, sticky="wens")


    def delete_user(self):
        if self.is_editing:
            self.unpaint_cards()
            self.main_instance.user_card = None
            self.main_instance.entry_name.delete(0,tk.END)
            self.main_instance.entry_mail.delete(0,tk.END)
        self.main_instance.user_card = None
        self.user_card_list.remove(self)
        if self.delete_callback:
            self.delete_callback(self.user_id)


    def update_user(self):
        self.unpaint_cards()
        self.edit_button.config(background="#FF0000")
        self.is_editing = not self.is_editing
        if self.is_editing:
            self.main_instance.user_card = self

            self.main_instance.entry_name.delete(0,tk.END)
            self.main_instance.entry_name.insert(0,self.name)

            self.main_instance.entry_mail.delete(0,tk.END)
            self.main_instance.entry_mail.insert(0,self.mail)

            self.main_instance.notebook.select(self.main_instance.add_tab)

        else:
            self.main_instance.user_card = None
            self.main_instance.entry_name.delete(0,tk.END)
            self.main_instance.entry_mail.delete(0,tk.END)
                        


    def unpaint_cards(self):
        for card in self.user_card_list:
            card.edit_button.config(background = "#0000FF")
            if card != self:
                card.is_editing = False


class MainView:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.user_card:UserCard = None
        self.init_wnd()


    def init_wnd(self):
        self.root.title("My Desktop App")

        title_label = tk.Label(self.root, text="Usuarios Random", font=("Helvetica", 12, "bold"))
        title_label.grid(column=0, row=0, sticky="nsew")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))

        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.grid(column=0, row=1, sticky="nsew")

        self.add_tab = ttk.Frame(self.notebook, padding=10)
        self.user_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.add_tab, text="Añadir usuario", sticky="wens")
        self.notebook.add(self.user_tab, text="Buscar usuario", sticky="wens")

        self.config_add_tab()
        self.config_user_tab()

        # Configuración del grid para root
        self.root.grid_rowconfigure(0, weight=1)  # El título ocupa solo una pequeña parte
        self.root.grid_rowconfigure(1, weight=10)  # El notebook se expande
        self.root.grid_columnconfigure(0, weight=1)


    def config_add_tab(self):
        # Configuración add_tab
        label_name = tk.Label(self.add_tab, text="Nombre")
        label_name.grid(row=0, column=0, sticky="wens")

        self.entry_name = tk.Entry(self.add_tab)
        self.entry_name.grid(row=1, column=0, sticky="wens")

        label_mail = tk.Label(self.add_tab, text="Correo")
        label_mail.grid(row=2, column=0, sticky="wens")

        self.entry_mail = tk.Entry(self.add_tab)
        self.entry_mail.grid(row=3, column=0, sticky="wens")

        add_button = tk.Button(self.add_tab, text="Guardar", command=lambda: self.add_user(self.entry_name.get(), self.entry_mail.get()))
        add_button.grid(row=4, column=0, sticky="wens")

        # Configuración del grid para add_tab
        self.add_tab.grid_rowconfigure(0, weight=1)
        self.add_tab.grid_rowconfigure(1, weight=1)
        self.add_tab.grid_rowconfigure(2, weight=1)
        self.add_tab.grid_rowconfigure(3, weight=1)
        self.add_tab.grid_rowconfigure(4, weight=1)

        self.add_tab.grid_columnconfigure(0, weight=1)


    def config_user_tab(self):
        # Show data
        self.filter_name_var = tk.StringVar()
        entry_filter_name = tk.Entry(self.user_tab, textvariable=self.filter_name_var)
        entry_filter_name.grid(row=0, column=0, sticky="we")
        self.filter_name_var.trace_add("write", self.update_view)

        self.canvas = tk.Canvas(self.user_tab)
        scrollbar_y = ttk.Scrollbar(self.user_tab, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar_y.set)

        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")

        # Configuración del grid para user_tab
        self.user_tab.grid_rowconfigure(0, weight=1)
        self.user_tab.grid_rowconfigure(1, weight=10)

        self.user_tab.grid_columnconfigure(0, weight=1)
        self.user_tab.grid_columnconfigure(1, weight=0)


    def set_controller(self, controller):
        self.controller = controller


    def fetch_data(self):
        self.controller.handle_fetch_data()


    def add_user(self, name, mail):
        nuevo_usuario = {
            'nombre': f'{name}',
            'correo': f'{mail}'
        }
        
        if self.user_card is not None:
            print("Editando user")
            user_id = self.user_card.user_id
            self.controller.update_user(user_id,nuevo_usuario)
        else:
            print("Nuevo user")
            self.controller.add_user(nuevo_usuario)
        self.entry_name.delete(0,tk.END)
        self.entry_mail.delete(0,tk.END)
        self.user_card = None


    def update_view(self,*args):
        value = self.filter_name_var.get()
        self.clean_frame(self.scrollable_frame)
        full_data = self.controller.handle_fetch_data(value)
        UserCard.user_card_list = []
        for idx, user in enumerate(full_data):
            user_id = user["id"]
            nombre = user["nombre"]
            correo = user["correo"]
            user_card = UserCard(master=self.scrollable_frame, 
                                 main_instance=self,
                                 user_id=user_id,
                                 name=nombre, 
                                 mail=correo,
                                 delete_callback=self.controller.delete_user,
                                 update_callback=self.controller.update_user)
            user_card.grid(row=idx, column=0, pady=10)


    @staticmethod
    def clean_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()
