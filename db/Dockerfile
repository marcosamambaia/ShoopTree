# Usa a imagem oficial do PostgreSQL
FROM postgres:16

# Define variáveis de ambiente para usuário, senha e banco
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=shoopdb

# Copia o script de inicialização para dentro do container
COPY init.sql /docker-entrypoint-initdb.d/
