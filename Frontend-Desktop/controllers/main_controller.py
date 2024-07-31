from models.data_model import DataModel
from views.main_view import MainView
from services.api_service import ApiService
import tkinter as tk

class MainController:
    def __init__(self):
        self.model = DataModel()
        self.api_service = ApiService()
        self.root = tk.Tk()
        self.view = MainView(self.root)
        self.view.set_controller(self)
        self.view.update_view()

    def handle_fetch_data(self,letra=""):
        data = self.api_service.get_data(letra=letra)
        self.model.add_data(data)
        all_data = self.model.get_data()
        return data

    def add_user(self,new_user):
        self.api_service.add_user(new_user)
        self.view.update_view()

    def update_user(self,user_id,updated_user):
        self.api_service.update_user(user_id=user_id,updated_user=updated_user)
        self.view.update_view()

    def delete_user(self,user_id):
        self.api_service.delete_user(user_id=user_id)
        self.view.update_view()


    def run(self):
        self.root.mainloop()
