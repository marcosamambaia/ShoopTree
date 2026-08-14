# Usa a imagem oficial do PostgreSQL
FROM postgres:16

# Define variáveis de ambiente para usuário, senha e banco
ENV POSTGRES_USER=marco
ENV POSTGRES_PASSWORD=marco123
ENV POSTGRES_DB=shoopdb


# Copia o script de inicialização para dentro do container
COPY init.sql /docker-entrypoint-initdb.d/
