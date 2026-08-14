CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco NUMERIC(10,2) NOT NULL,
    quantidade INT NOT NULL
);

CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    produto_id INT NOT NULL REFERENCES produtos(id),
    quantidade INT NOT NULL
);

CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    compra_id INT NOT NULL REFERENCES compras(id),
    valor NUMERIC(10,2) NOT NULL
);

CREATE TABLE notificacoes (
    id SERIAL PRIMARY KEY,
    compra_id INT NOT NULL REFERENCES compras(id),
    mensagem TEXT NOT NULL
);
