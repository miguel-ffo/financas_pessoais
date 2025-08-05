# -*- coding: utf-8 -*-
# ui/transaction_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from logic import app_logic # Importamos nosso novo módulo de lógica

class TransactionView(tk.Toplevel):
    # O 'refresh_callback' é uma função que será passada pela MainView
    # para que possamos "avisá-la" quando uma nova transação for salva.
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.parent = parent
        self.refresh_callback = refresh_callback # Armazenamos a função de callback
        
        self.title("Adicionar Nova Transação")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.tipo_var = tk.StringVar(value='despesa')
        self.descricao_var = tk.StringVar()
        self.valor_var = tk.StringVar()
        self.data_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.categoria_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(main_frame, textvariable=self.tipo_var, values=['despesa', 'receita'], state="readonly")
        tipo_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        descricao_entry = ttk.Entry(main_frame, textvariable=self.descricao_var)
        descricao_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        descricao_entry.focus_set() # Foco inicial no campo de descrição

        ttk.Label(main_frame, text="Valor (R$):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        valor_entry = ttk.Entry(main_frame, textvariable=self.valor_var)
        valor_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Data:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        data_entry = ttk.Entry(main_frame, textvariable=self.data_var)
        data_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Categoria:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        # Agora carregamos as categorias dinamicamente!
        categorias = app_logic.carregar_categorias()
        self.categoria_combo = ttk.Combobox(main_frame, textvariable=self.categoria_var, values=categorias, state="readonly")
        if categorias:
            self.categoria_combo.set(categorias[0]) # Seleciona a primeira como padrão
        self.categoria_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_button = ttk.Button(button_frame, text="Salvar", command=self.save)
        save_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)
    
    def save(self):
        """Coleta os dados do formulário e os envia para a camada de lógica."""
        dados = {
            'tipo': self.tipo_var.get(),
            'descricao': self.descricao_var.get(),
            'valor': self.valor_var.get(),
            'data': self.data_var.get(),
            'categoria': self.categoria_var.get()
        }
        
        sucesso, mensagem = app_logic.salvar_nova_transacao(dados)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self.refresh_callback() # Chama a função para atualizar a tabela na MainView
            self.destroy() # Fecha a janela de transação
        else:
            messagebox.showerror("Erro de Validação", mensagem, parent=self)

# O bloco de teste if __name__ == '__main__': não é mais necessário aqui,
# pois agora sempre abrimos esta janela a partir da MainView. Você pode removê-lo.