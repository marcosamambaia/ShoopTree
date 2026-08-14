from fastapi import FastAPI
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

class Pagamento(BaseModel):
    compra_id: int
    valor: float

@app.get("/pagamentos")
def listar_pagamentos():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, compra_id, valor FROM pagamentos")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "compra_id": r[1], "valor": float(r[2])} for r in rows]

@app.post("/pagamentos")
def registrar_pagamento(pagamento: Pagamento):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pagamentos (compra_id, valor) VALUES (%s, %s) RETURNING id",
        (pagamento.compra_id, pagamento.valor)
    )
    novo_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    # Dispara evento de pagamento confirmado
    event_bus.publish("PAGAMENTO_CONFIRMADO", {
        "id": novo_id,
        "compra_id": pagamento.compra_id,
        "valor": pagamento.valor
    })

    return {"mensagem": "Pagamento registrado com sucesso!", "id": novo_id}
