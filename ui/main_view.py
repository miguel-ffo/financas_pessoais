# -*- coding: utf-8 -*-
# ui/main_view.py

import tkinter as tk
from tkinter import ttk

# Importações do Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.transaction_view import TransactionView
from logic import app_logic

# Define um estilo mais agradável para os gráficos
plt.style.use('seaborn-v0_8-pastel')

class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.pack(expand=True, fill=tk.BOTH)
        
        self.create_widgets()
        self.refresh_view() # Renomeado de refresh_treeview para atualizar tudo

    def create_widgets(self):
        # --- Frame para ações e gráficos ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5, expand=False)
        
        action_frame = ttk.Frame(top_frame)
        action_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        add_button = ttk.Button(action_frame, text="Adicionar Transação", command=self.open_add_transaction)
        add_button.pack(pady=5)
        
        # Frame que vai conter os gráficos
        self.charts_frame = ttk.Frame(top_frame)
        self.charts_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # --- Frame para a lista de transações (agora na parte de baixo) ---
        list_frame = ttk.LabelFrame(self, text="Transações Recentes", padding="10")
        list_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Configuração da Treeview (sem alterações aqui)
        self.tree = ttk.Treeview(list_frame, columns=('Data', 'Tipo', 'Descrição', 'Valor', 'Categoria'), show='headings')
        self.tree.heading('Data', text='Data'); self.tree.heading('Tipo', text='Tipo'); self.tree.heading('Descrição', text='Descrição'); self.tree.heading('Valor', text='Valor (R$)'); self.tree.heading('Categoria', text='Categoria')
        self.tree.column('Data', width=100, anchor=tk.CENTER); self.tree.column('Tipo', width=80, anchor=tk.CENTER); self.tree.column('Descrição', width=250); self.tree.column('Valor', width=100, anchor=tk.E); self.tree.column('Categoria', width=120)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_view(self):
        """Atualiza todos os elementos da tela: a tabela e os gráficos."""
        self.refresh_treeview()
        self.refresh_charts()

    def refresh_treeview(self):
        """Limpa e recarrega a tabela com dados do banco."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        transacoes = app_logic.carregar_transacoes()
        for transacao in transacoes:
            valor_formatado = f"{transacao['valor']:.2f}"
            self.tree.insert('', tk.END, values=(transacao['data_transacao'], transacao['tipo'].capitalize(), transacao['descricao'], valor_formatado, transacao['categoria_nome']))

    def refresh_charts(self):
        """Limpa e recria os gráficos com os dados mais recentes."""
        # Limpa o frame de gráficos antes de adicionar novos
        for widget in self.charts_frame.winfo_children():
            widget.destroy()

        # --- Gráfico 1: Despesas por Categoria (Pizza) ---
        dados_gastos = app_logic.get_dados_gastos_categoria()
        if dados_gastos:
            fig_pie = plt.Figure(figsize=(4.5, 3), dpi=80)
            ax_pie = fig_pie.add_subplot(111)
            ax_pie.pie(dados_gastos.values(), labels=dados_gastos.keys(), autopct='%1.1f%%', startangle=90)
            ax_pie.set_title("Gastos por Categoria")
            fig_pie.tight_layout()

            canvas_pie = FigureCanvasTkAgg(fig_pie, master=self.charts_frame)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Gráfico 2: Balanço Receitas vs. Despesas (Barras) ---
        dados_balanco = app_logic.get_dados_balanco()
        if dados_balanco['Receitas'] > 0 or dados_balanco['Despesas'] > 0:
            fig_bar = plt.Figure(figsize=(4.5, 3), dpi=80)
            ax_bar = fig_bar.add_subplot(111)
            ax_bar.bar(dados_balanco.keys(), dados_balanco.values(), color=['#4CAF50', '#F44336'])
            ax_bar.set_title("Balanço: Receitas vs. Despesas")
            ax_bar.set_ylabel("Valor (R$)")
            fig_bar.tight_layout()

            canvas_bar = FigureCanvasTkAgg(fig_bar, master=self.charts_frame)
            canvas_bar.draw()
            canvas_bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def open_add_transaction(self):
        """Abre a janela de transação, passando a função de refresh como callback."""
        TransactionView(self.parent, self.refresh_view)