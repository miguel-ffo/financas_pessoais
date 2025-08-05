-- Tabela de Categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

-- Tabela de Transações
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data_transacao TEXT NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);

-- Inserir algumas categorias padrão para começar
INSERT OR IGNORE INTO categorias (nome) VALUES ('Alimentação'), ('Transporte'), ('Moradia'), ('Lazer'), ('Saúde'), ('Outros');