# shoop_api/main.py

from fastapi import FastAPI
import requests
# Importa o barramento de eventos e os consumidores que criamos em event_bus.py
from simulacao_eventos.event_bus import EventBus, PagamentoConsumer, NotificacaoConsumer

# Cria a aplicação FastAPI
app = FastAPI(title="ShoopTree API Gateway")

# Instancia o barramento de eventos (Observer)
event_bus = EventBus()

# Inscreve os consumidores no barramento
event_bus.subscribe(PagamentoConsumer())
event_bus.subscribe(NotificacaoConsumer())

# Endpoint para criar uma compra
@app.post("/compras")
def criar_compra(produto_id: int, quantidade: int):
    # Cria um evento do tipo COMPRA
    evento = {"tipo": "COMPRA", "produto_id": produto_id, "quantidade": quantidade}
    # Publica o evento no barramento
    event_bus.publish(evento)
    return {"status": "Compra registrada", "evento": evento}

# Endpoint para listar todos os eventos publicados
@app.get("/eventos")
def listar_eventos():
    return event_bus.historico
