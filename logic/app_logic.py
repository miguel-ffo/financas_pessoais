# -*- coding: utf-8 -*-
# logic/app_logic.py

from database import database_handler

def carregar_transacoes():
    """Pede ao handler do DB todas as transações e as retorna."""
    return database_handler.get_all_transacoes()

def carregar_categorias():
    """Pede ao handler do DB todas as categorias e as retorna."""
    categorias_rows = database_handler.get_categorias()
    return [row['nome'] for row in categorias_rows]

def salvar_nova_transacao(dados_transacao):
    """
    Recebe os dados da UI, valida, e se tudo estiver OK,
    pede ao handler do DB para salvar.
    """
    if not dados_transacao['descricao'] or not dados_transacao['valor'] or not dados_transacao['data']:
        return False, "Descrição, Valor e Data são obrigatórios."

    try:
        valor_float = float(dados_transacao['valor'].replace(',', '.'))
    except ValueError:
        return False, "O valor deve ser um número válido."
    
    categorias = database_handler.get_categorias()
    categoria_id = None
    for cat in categorias:
        if cat['nome'] == dados_transacao['categoria']:
            categoria_id = cat['id']
            break

    if categoria_id is None:
        return False, "Categoria inválida."

    try:
        database_handler.add_transacao(
            tipo=dados_transacao['tipo'],
            descricao=dados_transacao['descricao'],
            valor=valor_float,
            data_transacao=dados_transacao['data'],
            categoria_id=categoria_id
        )
        return True, "Transação salva com sucesso!"
    except Exception as e:
        return False, "Ocorreu um erro ao salvar no banco de dados."

# --- NOVAS FUNÇÕES PARA OS GRÁFICOS ---

def get_dados_gastos_categoria():
    """Busca e processa os dados de despesas por categoria para o gráfico de pizza."""
    transacoes = database_handler.get_all_transacoes()
    dados = {}
    for t in transacoes:
        if t['tipo'] == 'despesa':
            categoria = t['categoria_nome']
            valor = t['valor']
            if categoria in dados:
                dados[categoria] += valor
            else:
                dados[categoria] = valor
    return dados

def get_dados_balanco():
    """Busca e processa o balanço total de receitas e despesas."""
    transacoes = database_handler.get_all_transacoes()
    balanco = {'Receitas': 0, 'Despesas': 0}
    for t in transacoes:
        if t['tipo'] == 'receita':
            balanco['Receitas'] += t['valor']
        else:
            balanco['Despesas'] += t['valor']
    return balanco

# logic/app_logic.py

# ... (todo o código existente até o final de salvar_nova_transacao) ...

# --- NOVAS FUNÇÕES PARA EDITAR E EXCLUIR ---

def get_transacao(id_transacao):
    """Busca os dados de uma única transação."""
    return database_handler.get_transacao_por_id(id_transacao)

def atualizar_transacao(id_transacao, dados_transacao):
    """Valida e envia dados para atualizar uma transação."""
    # A mesma validação da criação
    if not dados_transacao['descricao'] or not dados_transacao['valor'] or not dados_transacao['data']:
        return False, "Descrição, Valor e Data são obrigatórios."
    try:
        valor_float = float(dados_transacao['valor'].replace(',', '.'))
    except ValueError:
        return False, "O valor deve ser um número válido."
    
    categorias = database_handler.get_categorias()
    categoria_id = next((cat['id'] for cat in categorias if cat['nome'] == dados_transacao['categoria']), None)
    if categoria_id is None:
        return False, "Categoria inválida."

    try:
        database_handler.update_transacao(
            id_transacao,
            dados_transacao['tipo'],
            dados_transacao['descricao'],
            valor_float,
            dados_transacao['data'],
            categoria_id
        )
        return True, "Transação atualizada com sucesso!"
    except Exception as e:
        return False, f"Ocorreu um erro ao atualizar: {e}"

def remover_transacao(id_transacao):
    """Envia uma requisição para remover uma transação."""
    try:
        database_handler.delete_transacao(id_transacao)
        return True, "Transação removida com sucesso."
    except Exception as e:
        return False, f"Ocorreu um erro ao remover: {e}"