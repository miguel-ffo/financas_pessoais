# -*- coding: utf-8 -*-
# ui/transaction_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from logic import app_logic

class TransactionView(tk.Toplevel):
    def __init__(self, parent, refresh_callback, transaction_id=None):
        super().__init__(parent)
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.transaction_id = transaction_id

        if self.transaction_id:
            self.title("Editar Transação")
        else:
            self.title("Adicionar Nova Transação")

        self.geometry("400x320") # Aumentei um pouco a altura para melhor espaçamento
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # --- NOVO: Configurando Estilos ---
        self.setup_styles()
        
        self.create_widgets()

        if self.transaction_id:
            self.load_transaction_data()

        self.center_window()

    def setup_styles(self):
        """Define estilos personalizados para os widgets desta janela."""
        style = ttk.Style(self)
        
        # Estilo para o botão de sucesso (Salvar)
        style.configure('Success.TButton', font=('Helvetica', 10, 'bold'), background='#2ECC71', foreground='white')
        style.map('Success.TButton', 
            background=[('active', '#28B463')], 
            foreground=[('active', 'white')]
        )
        
        # Estilo para o botão padrão (Cancelar)
        style.configure('Standard.TButton', font=('Helvetica', 10))

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # ... (código de criação de labels e campos, sem alterações) ...
        self.tipo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.valor_var = tk.StringVar()
        self.data_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        ttk.Label(main_frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        tipo_combo = ttk.Combobox(main_frame, textvariable=self.tipo_var, values=['despesa', 'receita'], state="readonly")
        tipo_combo.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        ttk.Label(main_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        descricao_entry = ttk.Entry(main_frame, textvariable=self.descricao_var)
        descricao_entry.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        descricao_entry.focus_set()
        ttk.Label(main_frame, text="Valor (R$):").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        valor_entry = ttk.Entry(main_frame, textvariable=self.valor_var)
        valor_entry.grid(row=2, column=1, padx=5, pady=8, sticky="ew")
        ttk.Label(main_frame, text="Data:").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        self.data_entry = DateEntry(main_frame, textvariable=self.data_var, date_pattern='yyyy-mm-dd', width=12)
        self.data_entry.grid(row=3, column=1, padx=5, pady=8, sticky="ew")
        ttk.Label(main_frame, text="Categoria:").grid(row=4, column=0, padx=5, pady=8, sticky="w")
        categorias = app_logic.carregar_categorias()
        self.categoria_combo = ttk.Combobox(main_frame, textvariable=self.categoria_var, values=categorias, state="readonly")
        self.categoria_combo.grid(row=4, column=1, padx=5, pady=8, sticky="ew")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 5))
        
        # Aplicando os novos estilos aos botões
        save_button = ttk.Button(button_frame, text="Salvar", command=self.save, style='Success.TButton')
        save_button.pack(side=tk.LEFT, padx=10, ipady=4)
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy, style='Standard.TButton')
        cancel_button.pack(side=tk.LEFT, padx=10, ipady=4)

    # ... (O resto do arquivo: center_window, load_transaction_data, save - permanecem iguais) ...
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_transaction_data(self):
        transacao = app_logic.get_transacao(self.transaction_id)
        if not transacao:
            messagebox.showerror("Erro", "Transação não encontrada.", parent=self)
            self.destroy()
            return
        categoria_obj = next((cat for cat in app_logic.database_handler.get_categorias() if cat['id'] == transacao['categoria_id']), None)
        self.tipo_var.set(transacao['tipo'])
        self.descricao_var.set(transacao['descricao'])
        self.valor_var.set(f"{transacao['valor']:.2f}")
        self.data_var.set(transacao['data_transacao'])
        if categoria_obj:
            self.categoria_var.set(categoria_obj['nome'])

    def save(self):
        dados = { 'tipo': self.tipo_var.get(), 'descricao': self.descricao_var.get(), 'valor': self.valor_var.get(), 'data': self.data_var.get(), 'categoria': self.categoria_var.get() }
        if self.transaction_id:
            sucesso, mensagem = app_logic.atualizar_transacao(self.transaction_id, dados)
        else:
            sucesso, mensagem = app_logic.salvar_nova_transacao(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", mensagem, parent=self)