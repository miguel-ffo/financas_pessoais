# -*- coding: utf-8 -*-
# logic/app_logic.py

from database import database_handler

def carregar_transacoes():
    """Pede ao handler do DB todas as transações e as retorna."""
    return database_handler.get_all_transacoes()

def carregar_categorias():
    """Pede ao handler do DB todas as categorias e as retorna."""
    # Retornamos apenas os nomes para usar no combobox da UI
    categorias_rows = database_handler.get_categorias()
    return [row['nome'] for row in categorias_rows]

def salvar_nova_transacao(dados_transacao):
    """
    Recebe os dados da UI, valida, e se tudo estiver OK,
    pede ao handler do DB para salvar.
    """
    # Validação básica
    if not dados_transacao['descricao'] or not dados_transacao['valor'] or not dados_transacao['data']:
        return False, "Descrição, Valor e Data são obrigatórios."

    try:
        # Tenta converter o valor para float
        valor_float = float(dados_transacao['valor'].replace(',', '.'))
    except ValueError:
        return False, "O valor deve ser um número válido."
    
    # Busca o ID da categoria a partir do nome
    categorias = database_handler.get_categorias()
    categoria_id = None
    for cat in categorias:
        if cat['nome'] == dados_transacao['categoria']:
            categoria_id = cat['id']
            break

    if categoria_id is None:
        return False, "Categoria inválida."

    # Se tudo estiver ok, chama o handler do banco
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
        # Em um app real, seria bom logar o erro 'e'
        return False, "Ocorreu um erro ao salvar no banco de dados."