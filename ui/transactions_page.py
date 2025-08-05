# -*- coding: utf-8 -*-
# ui/transactions_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.transaction_view import TransactionView
from logic import app_logic

class TransactionsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.create_widgets()
        
        # --- ALTERAÇÃO AQUI: Invertendo as cores ---
        # Fundo escuro e fonte clara para melhor contraste
        self.tree.tag_configure('receita_tag', background='#196F3D', foreground='white')
        self.tree.tag_configure('despesa_tag', background='#A93226', foreground='white')

    def create_widgets(self):
        # ... (todo o resto do seu código permanece exatamente igual) ...
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, pady=5, padx=5)
        
        add_button = ttk.Button(action_frame, text="Adicionar Transação", command=self.open_add_transaction)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = ttk.Button(action_frame, text="Excluir Selecionada", command=self.delete_selected_transaction)
        delete_button.pack(side=tk.LEFT)

        list_frame = ttk.LabelFrame(self, text="Histórico de Transações", padding="10")
        list_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=5)
        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Data', 'Tipo', 'Descrição', 'Valor', 'Categoria'), show='headings')
        
        self.tree.heading('ID', text='ID'); self.tree.heading('Data', text='Data'); self.tree.heading('Tipo', text='Tipo'); self.tree.heading('Descrição', text='Descrição'); self.tree.heading('Valor', text='Valor (R$)'); self.tree.heading('Categoria', text='Categoria')
        self.tree.column('ID', width=0, stretch=tk.NO); self.tree.column('Data', width=100, anchor=tk.CENTER); self.tree.column('Tipo', width=80, anchor=tk.CENTER); self.tree.column('Descrição', width=300); self.tree.column('Valor', width=100, anchor=tk.E); self.tree.column('Categoria', width=150)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<Double-1>", self.on_double_click)

    def refresh_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        transacoes = app_logic.carregar_transacoes()
        for transacao in transacoes:
            valor_formatado = f"{transacao['valor']:.2f}"
            tag_usada = 'receita_tag' if transacao['tipo'] == 'receita' else 'despesa_tag'
            self.tree.insert('', tk.END, values=(
                transacao['id'], transacao['data_transacao'], transacao['tipo'].capitalize(),
                transacao['descricao'], valor_formatado, transacao['categoria_nome']
            ), tags=(tag_usada,))

    def on_double_click(self, event):
        if not self.tree.selection():
            return
        item_id = self.tree.selection()[0]
        transaction_id = self.tree.item(item_id, "values")[0]
        TransactionView(self.parent, self.refresh_view, transaction_id=transaction_id)

    def delete_selected_transaction(self):
        if not self.tree.selection():
            messagebox.showwarning("Atenção", "Por favor, selecione uma transação para excluir.")
            return
        item_id = self.tree.selection()[0]
        transaction_id = self.tree.item(item_id, "values")[0]
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir esta transação?"):
            sucesso, mensagem = app_logic.remover_transacao(transaction_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.refresh_view()
            else:
                messagebox.showerror("Erro", mensagem)

    def open_add_transaction(self):
        TransactionView(self.parent, self.refresh_view)