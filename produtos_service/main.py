# Importa o framework FastAPI para criar a API
from fastapi import FastAPI
# Importa BaseModel do Pydantic para validar dados recebidos
from pydantic import BaseModel
# Importa biblioteca psycopg2 para conectar ao PostgreSQL e os para variáveis de ambiente
import psycopg2, os

# Cria a aplicação FastAPI
app = FastAPI()

# URL de conexão ao banco de dados
# Se não for definida via variável de ambiente, usa o valor padrão
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@db:5432/shoopdb")

# Modelo de dados para representar um Produto
class Produto(BaseModel):
    nome: str

# Endpoint GET /produtos
# Lista todos os produtos cadastrados no banco
@app.get("/produtos")
def listar_produtos():
    # Conecta ao banco
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Executa consulta SQL
    cur.execute("SELECT id, nome FROM produtos")
    rows = cur.fetchall()
    # Fecha conexão
    conn.close()
    # Retorna lista de produtos em formato JSON
    return [{"id": r[0], "nome": r[1]} for r in rows]

# Endpoint POST /produtos
# Adiciona um novo produto ao banco
@app.post("/produtos")
def adicionar_produto(produto: Produto):
    # Conecta ao banco
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Insere produto e retorna o ID gerado
    cur.execute("INSERT INTO produtos (nome) VALUES (%s) RETURNING id", (produto.nome,))
