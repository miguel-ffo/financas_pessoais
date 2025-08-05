# -*- coding: utf-8 -*-
# ui/main_view.py

import tkinter as tk
from tkinter import ttk
from ui.transaction_view import TransactionView
from logic import app_logic # Importamos nosso módulo de lógica

class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.pack(expand=True, fill=tk.BOTH)
        self.create_widgets()
        # Carrega os dados na tabela assim que a aplicação inicia
        self.refresh_treeview()

    def create_widgets(self):
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, pady=5)
        add_button = ttk.Button(action_frame, text="Adicionar Transação", command=self.open_add_transaction)
        add_button.pack(side=tk.LEFT)

        list_frame = ttk.LabelFrame(self, text="Transações Recentes", padding="10")
        list_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        self.tree = ttk.Treeview(list_frame, columns=('Data', 'Tipo', 'Descrição', 'Valor', 'Categoria'), show='headings')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Valor', text='Valor (R$)')
        self.tree.heading('Categoria', text='Categoria')
        self.tree.column('Data', width=100, anchor=tk.CENTER)
        self.tree.column('Tipo', width=80, anchor=tk.CENTER)
        self.tree.column('Descrição', width=200)
        self.tree.column('Valor', width=100, anchor=tk.E)
        self.tree.column('Categoria', width=120)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_treeview(self):
        """Limpa a tabela e a recarrega com os dados do banco."""
        # Limpa todos os itens existentes na árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Carrega os dados usando a camada de lógica
        transacoes = app_logic.carregar_transacoes()
        
        # Insere os novos dados na árvore
        for transacao in transacoes:
            valor_formatado = f"{transacao['valor']:.2f}"
            self.tree.insert('', tk.END, values=(
                transacao['data_transacao'],
                transacao['tipo'].capitalize(), # 'despesa' -> 'Despesa'
                transacao['descricao'],
                valor_formatado,
                transacao['categoria_nome']
            ))

    def open_add_transaction(self):
        """
        Abre a janela de transação, passando a função de refresh
        como um 'callback'.
        """
        # Passamos a nossa própria função 'refresh_treeview' como argumento.
        # A TransactionView vai chamar essa função quando uma transação for salva.
        TransactionView(self.parent, self.refresh_treeview)