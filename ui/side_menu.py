# -*- coding: utf-8 -*-
# ui/side_menu.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ui.dashboard_page import DashboardPage
from ui.transactions_page import TransactionsPage

class SideMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Estilizando o frame do menu
        self.config(style='Side.TFrame')
        style = ttk.Style()
        style.configure('Side.TFrame', background='#e0e0e0')
        style.configure('Side.TButton', font=('Helvetica', 12), padding=10, anchor="w") # anchor="w" alinha o texto à esquerda
        style.map('Side.TButton',
            background=[('active', '#cccccc')],
            foreground=[('active', 'black')]
        )
        
        self.create_widgets()
    
    def load_icon(self, path, size):
        """Função auxiliar para carregar ícones e evitar crashes se o arquivo não existir."""
        try:
            # Use .png em vez de .svg
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Erro: Ícone não encontrado em '{path}'")
            return None

    def create_widgets(self):
        """Cria os botões de navegação com ícones e texto."""

        # --- Botão Dashboard ---
        self.dashboard_icon = self.load_icon("assets/icons/home.png", (20, 20))
        btn_dashboard = ttk.Button(self, text="  Dashboard", image=self.dashboard_icon, compound=tk.LEFT, style='Side.TButton',
                                   command=lambda: self.controller.show_frame(DashboardPage))
        btn_dashboard.pack(fill=tk.X, padx=5, pady=(10, 5))
        
        # --- Botão Transações ---
        self.transactions_icon = self.load_icon("assets/icons/list.png", (20, 20))
        btn_transactions = ttk.Button(self, text="  Transações", image=self.transactions_icon, compound=tk.LEFT, style='Side.TButton',
                                      command=lambda: self.controller.show_frame(TransactionsPage))
        btn_transactions.pack(fill=tk.X, padx=5, pady=5)