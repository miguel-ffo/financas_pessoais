# -*- coding: utf-8 -*-
# main.py

import tkinter as tk
from ui.main_view import MainView
from database.database_handler import init_db

class App(tk.Tk):
    """Classe principal da aplicação."""
    def __init__(self):
        super().__init__()

        self.title("Finanças Pessoais Desktop")
        self.geometry("800x600")

        # Chama a MainView e a coloca dentro da janela principal
        self.main_view = MainView(self)

if __name__ == '__main__':
    # Garante que o banco de dados e as tabelas existam antes de iniciar a UI
    print("Inicializando o banco de dados...")
    init_db()
    
    print("Iniciando a aplicação...")
    app = App()
    app.mainloop()