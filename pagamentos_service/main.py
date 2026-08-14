from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# Usa variável de ambiente ou valor padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=shoopdb user=marco password=marco123 host=db port=5432"
)

class Pagamento(BaseModel):
    produto_id: int
    quantidade: int
    valor: float

@app.get("/pagamentos")
def listar_pagamentos():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, produto_id, quantidade, valor FROM pagamentos")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "produto_id": r[1], "quantidade": r[2], "valor": float(r[3])} for r in rows]

@app.post("/pagamentos")
def registrar_pagamento(pagamento: Pagamento):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Busca produto
    cur.execute("SELECT preco, quantidade FROM produtos WHERE id = %s", (pagamento.produto_id,))
    produto = cur.fetchone()
    if not produto:
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    preco, estoque = produto
    valor_esperado = preco * pagamento.quantidade

    # Valida valor
    if pagamento.valor != valor_esperado:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Valor incorreto. Esperado: {valor_esperado}")

    # Valida estoque
    if pagamento.quantidade > estoque:
        conn.close()
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    # Atualiza estoque
    novo_estoque = estoque - pagamento.quantidade
    cur.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (novo_estoque, pagamento.produto_id))

    # Registra pagamento
    cur.execute(
        "INSERT INTO pagamentos (produto_id, quantidade, valor) VALUES (%s, %s, %s) RETURNING id",
        (pagamento.produto_id, pagamento.quantidade, pagamento.valor)
    )
    novo_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return {"mensagem": "Pagamento registrado com sucesso!", "id": novo_id}
