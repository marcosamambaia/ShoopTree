from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# Usa variável de ambiente ou valor padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=shoopdb user=marco password=marco123 host=db port=5432"
)

class Produto(BaseModel):
    nome: str
    preco: float
    quantidade: int

@app.get("/produtos")
def listar_produtos():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco, quantidade FROM produtos")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "nome": r[1],
            "preco": float(r[2]) if r[2] is not None else None,
            "quantidade": r[3] if r[3] is not None else None
        }
        for r in rows
    ]

@app.post("/produtos")
def adicionar_produto(produto: Produto):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s) RETURNING id",
        (produto.nome, produto.preco, produto.quantidade)
    )
    novo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"mensagem": "Produto adicionado com sucesso!", "id": novo_id}
