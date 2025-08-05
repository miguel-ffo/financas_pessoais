# -*- coding: utf-8 -*-
# database/database_handler.py


import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'financeiro.db')

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados, criando as tabelas necessárias se não existirem."""
    
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transacoes'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        with open(schema_file, 'r', encoding='utf-8') as f:            conn.executescript(f.read())
        conn.commit()
        print("Banco de dados criado com sucesso.")
    else:
        print("Banco de dados já existe.")
    
    conn.close()
    
    
def get_categorias():
    """Busca todas as categorias no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    conn.close()
    return categorias


# --- Funções para Transações ---

def add_transacao(tipo, descricao, valor, data_transacao, categoria_id):
    """
    Adiciona uma nova transação ao banco de dados.
    Usamos '?' como placeholders para evitar SQL Injection.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transacoes (tipo, descricao, valor, data_transacao, categoria_id) VALUES (?, ?, ?, ?, ?)",
        (tipo, descricao, valor, data_transacao, categoria_id)
    )
    conn.commit()
    conn.close()

def get_all_transacoes():
    """
    Busca todas as transações, juntando com o nome da categoria correspondente.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Usamos um LEFT JOIN para que, mesmo se uma transação não tiver categoria, ela ainda apareça
    cursor.execute("""
        SELECT 
            t.id, 
            t.tipo, 
            t.descricao, 
            t.valor, 
            t.data_transacao, 
            c.nome as categoria_nome
        FROM 
            transacoes t
        LEFT JOIN 
            categorias c ON t.categoria_id = c.id
        ORDER BY 
            t.data_transacao DESC
    """)
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

# --- Bloco de Teste ---
# Este código só será executado se você rodar este arquivo diretamente (python database/database_handler.py)
# É uma ótima forma de testar se as funções estão funcionando sem precisar da aplicação completa.
if __name__ == '__main__':
    print("Executando testes do database_handler...")
    
    # 1. Inicializa o banco de dados (deve criar o arquivo financeiro.db na primeira vez)
    init_db()
    
    # 2. Busca e imprime as categorias
    print("\n--- Categorias Disponíveis ---")
    categorias = get_categorias()
    if categorias:
        # A primeira categoria será usada para o teste de adição de transação
        primeira_categoria_id = categorias[0]['id']
        for categoria in categorias:
            print(f"ID: {categoria['id']}, Nome: {categoria['nome']}")
    else:
        print("Nenhuma categoria encontrada.")
        primeira_categoria_id = None

    # 3. Adiciona uma transação de teste, se houver categorias
    if primeira_categoria_id is not None:
        print("\n--- Adicionando Transação de Teste ---")
        try:
            add_transacao('despesa', 'Café da tarde', 12.50, '2025-08-05', primeira_categoria_id)
            print("Transação de teste adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")

    # 4. Busca e imprime todas as transações
    print("\n--- Todas as Transações no Banco ---")
    todas_as_transacoes = get_all_transacoes()
    if todas_as_transacoes:
        for transacao in todas_as_transacoes:
            # Monta um dicionário simples para facilitar a impressão
            print(dict(transacao))
    else:
        print("Nenhuma transação encontrada.")    