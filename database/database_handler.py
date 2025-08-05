# -*- coding: utf-8 -*-
# database/database_handler.py

import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'financeiro.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # ... (código existente, sem alterações) ...
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transacoes'")
    table_exists = cursor.fetchone()
    if not table_exists:
        print("Criando o banco de dados inicial...")
        with open(schema_file, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Banco de dados criado com sucesso.")
    else:
        print("O banco de dados já existe.")
    conn.close()

# --- Funções de Categoria (sem alterações) ---
def get_categorias():
    # ... (código existente, sem alterações) ...
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    conn.close()
    return categorias

# --- Funções de Transações (com adições) ---
def add_transacao(tipo, descricao, valor, data_transacao, categoria_id):
    # ... (código existente, sem alterações) ...
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (tipo, descricao, valor, data_transacao, categoria_id) VALUES (?, ?, ?, ?, ?)",
        (tipo, descricao, valor, data_transacao, categoria_id)
    )
    conn.commit()
    conn.close()

def get_all_transacoes():
    # ... (código existente, sem alterações) ...
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.tipo, t.descricao, t.valor, t.data_transacao, c.nome as categoria_nome
        FROM transacoes t LEFT JOIN categorias c ON t.categoria_id = c.id
        ORDER BY t.data_transacao DESC, t.id DESC
    """)
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

# --- NOVAS FUNÇÕES ---

def get_transacao_por_id(id_transacao):
    """Busca uma única transação pelo seu ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes WHERE id = ?", (id_transacao,))
    transacao = cursor.fetchone()
    conn.close()
    return transacao

def update_transacao(id_transacao, tipo, descricao, valor, data_transacao, categoria_id):
    """Atualiza uma transação existente no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transacoes
        SET tipo = ?, descricao = ?, valor = ?, data_transacao = ?, categoria_id = ?
        WHERE id = ?
    """, (tipo, descricao, valor, data_transacao, categoria_id, id_transacao))
    conn.commit()
    conn.close()

def delete_transacao(id_transacao):
    """Exclui uma transação do banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()