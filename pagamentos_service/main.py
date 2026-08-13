# Importa o framework FastAPI para criar a API
from fastapi import FastAPI
# Importa BaseModel do Pydantic para validar dados recebidos
from pydantic import BaseModel
# Importa psycopg2 para conectar ao PostgreSQL e os para variáveis de ambiente
import psycopg2, os

# Cria a aplicação FastAPI
app = FastAPI()

# URL de conexão ao banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@db:5432/shoopdb")

# Modelo de dados para representar um Pagamento
class Pagamento(BaseModel):
    valor: float

# Funções que simulam observadores (Observer Pattern)
def notificar_email(pagamento_id):
    print(f"Email enviado: pagamento {pagamento_id} registrado.")

def atualizar_estoque(pagamento_id):
    print(f"Estoque atualizado para pagamento {pagamento_id}.")

# Endpoint GET /pagamentos
# Lista todos os pagamentos cadastrados no banco
@app.get("/pagamentos")
def listar_pagamentos():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, valor FROM pagamentos")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "valor": float(r[1])} for r in rows]

# Endpoint POST /pagamentos
# Registra um novo pagamento e dispara eventos para os observadores
@app.post("/pagamentos")
def registrar_pagamento(pagamento: Pagamento):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Insere pagamento e retorna o ID gerado
    cur.execute("INSERT INTO pagamentos (valor) VALUES (%s) RETURNING id", (pagamento.valor,))
    pagamento_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    # Dispara eventos simulados (Observer Pattern)
    notificar_email(pagamento_id)
    atualizar_estoque(pagamento_id)

    return {"mensagem": "Pagamento registrado com sucesso!", "id": pagamento_id}
