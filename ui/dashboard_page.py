# -*- coding: utf-8 -*-
# ui/dashboard_page.py

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logic import app_logic

# Define uma paleta de cores moderna e profissional para os gráficos
COR_RECEITA = '#2ECC71'
COR_DESPESA = '#E74C3C'
COR_BALANCO = '#3498DB'
CORES_PIZZA = ['#3498DB', '#E74C3C', '#9B59B6', '#F1C40F', '#1ABC9C', '#E67E22', '#5DADE2', '#C0392B']

# Estilo para os gráficos
plt.style.use('seaborn-v0_8-whitegrid')

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def create_kpi_card(self, parent, title, value_str, title_color):
        """Função auxiliar para criar os cards de KPI de forma padronizada."""
        card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        lbl_title = ttk.Label(card, text=title, style='CardTitle.TLabel')
        lbl_title.pack(pady=(0, 5))
        lbl_title.configure(foreground=title_color)

        lbl_value = ttk.Label(card, text=value_str, style='CardValue.TLabel')
        lbl_value.pack()

    def refresh_view(self):
        """Atualiza todos os elementos da tela: os cards e os gráficos."""
        # Limpa o frame antes de recriar os componentes
        for widget in self.winfo_children():
            widget.destroy()

        # Estilos para os cards
        style = ttk.Style(self)
        style.configure('Card.TFrame', relief='raised', borderwidth=2)
        style.configure('CardTitle.TLabel', font=('Helvetica', 14, 'bold'))
        style.configure('CardValue.TLabel', font=('Helvetica', 22, 'bold'))

        # --- DADOS ---
        dados_balanco = app_logic.get_dados_balanco()
        dados_gastos = app_logic.get_dados_gastos_categoria()

        # Verifica se há transações. Se não, mostra uma mensagem.
        if not dados_balanco['Receitas'] and not dados_balanco['Despesas']:
            lbl_empty = ttk.Label(self, text="Adicione transações para ver seu dashboard!", font=('Helvetica', 18))
            lbl_empty.pack(expand=True)
            return

        # --- FRAME DOS CARDS (KPIs) ---
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill=tk.X, pady=10)

        receitas = dados_balanco['Receitas']
        despesas = dados_balanco['Despesas']
        balanco = receitas - despesas

        self.create_kpi_card(cards_frame, "Receitas Totais", f"R$ {receitas:,.2f}", COR_RECEITA)
        self.create_kpi_card(cards_frame, "Despesas Totais", f"R$ {despesas:,.2f}", COR_DESPESA)
        self.create_kpi_card(cards_frame, "Balanço Final", f"R$ {balanco:,.2f}", COR_BALANCO)

        # --- FRAME DOS GRÁFICOS ---
        charts_frame = ttk.Frame(self)
        charts_frame.pack(expand=True, fill=tk.BOTH)

        # Gráfico 1: Gastos por Categoria (Donut)
        if dados_gastos:
            fig_pie = plt.Figure(figsize=(5, 4), dpi=90)
            ax_pie = fig_pie.add_subplot(111)
            
            wedges, texts, autotexts = ax_pie.pie(dados_gastos.values(), 
                                                  labels=dados_gastos.keys(), 
                                                  autopct='%1.1f%%', 
                                                  startangle=140, 
                                                  colors=CORES_PIZZA,
                                                  pctdistance=0.85)
            # Transforma em Donut
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            ax_pie.add_artist(centre_circle)
            
            plt.setp(autotexts, size=8, weight="bold", color="white")
            ax_pie.set_title("Distribuição de Despesas", fontsize=14, weight='bold')
            fig_pie.tight_layout()

            canvas_pie = FigureCanvasTkAgg(fig_pie, master=charts_frame)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Gráfico 2: Balanço (Barras com Rótulos)
        if receitas > 0 or despesas > 0:
            fig_bar = plt.Figure(figsize=(5, 4), dpi=90)
            ax_bar = fig_bar.add_subplot(111)
            bars = ax_bar.bar(dados_balanco.keys(), dados_balanco.values(), color=[COR_RECEITA, COR_DESPESA])
            ax_bar.set_title("Balanço Geral", fontsize=14, weight='bold')
            ax_bar.set_ylabel("Valor (R$)")
            
            # Adiciona os rótulos no topo das barras
            for bar in bars:
                yval = bar.get_height()
                ax_bar.text(bar.get_x() + bar.get_width()/2.0, yval, f'R$ {yval:,.2f}', va='bottom', ha='center')

            fig_bar.tight_layout()

            canvas_bar = FigureCanvasTkAgg(fig_bar, master=charts_frame)
            canvas_bar.draw()
            canvas_bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)