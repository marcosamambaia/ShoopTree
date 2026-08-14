from fastapi import FastAPI
import psycopg2
import os
from event_bus import event_bus

app = FastAPI()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=shoopdb user=marco password=marco123 host=db port=5432"
)

# Lista notificações
@app.get("/notificacoes")
def listar_notificacoes():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, compra_id, mensagem FROM notificacoes")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "compra_id": r[1], "mensagem": r[2]} for r in rows]

# Handler para evento de pagamento confirmado
def handle_pagamento_confirmado(evento):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notificacoes (compra_id, mensagem) VALUES (%s, %s)",
        (evento["compra_id"], f"Pagamento confirmado para compra {evento['compra_id']}")
    )
    conn.commit()
    conn.close()
    print(f"[Notificação] Cliente informado sobre pagamento da compra {evento['compra_id']}")

# Inscreve no evento
event_bus.subscribe("PAGAMENTO_CONFIRMADO", handle_pagamento_confirmado)

from typing import List, Callable

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
