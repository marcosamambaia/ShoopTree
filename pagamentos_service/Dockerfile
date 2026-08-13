# Usa uma imagem base leve do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Comando padrão para iniciar o serviço na porta 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
