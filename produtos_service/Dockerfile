# Imagem base leve do Python
FROM python:3.12-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando padrão para iniciar o serviço
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
