# -*- coding: utf-8 -*-
# main.py

import tkinter as tk
from tkinter import ttk
import sv_ttk # Importa a biblioteca


# Importando os novos componentes de UI
from ui.side_menu import SideMenu
from ui.dashboard_page import DashboardPage
from ui.transactions_page import TransactionsPage

from database.database_handler import init_db

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Finanças Pessoais Desktop")
        self.geometry("1024x600")

        # Configura o layout principal da janela
        # A coluna do menu (0) terá um peso fixo, a do conteúdo (1) se expandirá
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Cria o Menu Lateral ---
        self.side_menu = SideMenu(self, self)
        self.side_menu.grid(row=0, column=0, sticky="ns")

        # --- Cria o Container para as Páginas ---
        container = ttk.Frame(self)
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Itera sobre as classes de página que queremos na nossa aplicação
        for F in (DashboardPage, TransactionsPage):
            page_name = F.__name__
            # Cria uma instância de cada página
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            # Coloca cada página no mesmo lugar no container.
            # A que for criada por último ficará no topo.
            frame.grid(row=0, column=0, sticky="nsew")

        # Inicia mostrando a tela do Dashboard
        self.show_frame(DashboardPage)

    def show_frame(self, page_class):
        '''Mostra um frame para a classe de página dada'''
        frame = self.frames[page_class]
        # Chama a função de refresh da página que está sendo exibida
        frame.refresh_view()
        # Traz o frame para a frente
        frame.tkraise()

if __name__ == '__main__':
    print("Inicializando o banco de dados...")
    init_db()
    
    print("Iniciando a aplicação...")
    app = App()
    sv_ttk.set_theme("dark") # OU "light" - Aplica o tema
    app.mainloop()