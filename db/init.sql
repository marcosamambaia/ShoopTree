-- Criação da tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco NUMERIC NOT NULL,
    quantidade INT NOT NULL
);

-- Criação da tabela de pagamentos
CREATE TABLE IF NOT EXISTS pagamentos (
    id SERIAL PRIMARY KEY,
    produto_id INT REFERENCES produtos(id),
    quantidade INT NOT NULL,
    valor NUMERIC NOT NULL
);
