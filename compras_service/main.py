from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from typing import Callable

app = FastAPI()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=shoopdb user=marco password=marco123 host=db port=5432"
)

# EventBus definido dentro do mesmo arquivo
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: dict):
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                handler(data)

# Instância global
event_bus = EventBus()

class Compra(BaseModel):
    produto_id: int
    quantidade: int

@app.get("/compras")
def listar_compras():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, produto_id, quantidade FROM compras")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "produto_id": r[1], "quantidade": r[2]} for r in rows]

@app.post("/compras")
def registrar_compra(compra: Compra):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT quantidade FROM produtos WHERE id = %s", (compra.produto_id,))
    produto = cur.fetchone()
    if not produto:
        conn.close()
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    estoque = produto[0]
    if compra.quantidade > estoque:
        conn.close()
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    novo_estoque = estoque - compra.quantidade
    cur.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (novo_estoque, compra.produto_id))

    cur.execute(
        "INSERT INTO compras (produto_id, quantidade) VALUES (%s, %s) RETURNING id",
        (compra.produto_id, compra.quantidade)
    )
    novo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    # Dispara evento de compra realizada
    event_bus.publish("COMPRA_REALIZADA", {"id": novo_id, "produto_id": compra.produto_id, "quantidade": compra.quantidade})

    return {"mensagem": "Compra registrada com sucesso!", "id": novo_id}
