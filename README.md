# ShoopTree - Prova de Conceito

##  Objetivo
Este projeto é uma prova de conceito funcional que demonstra:
- Dois microserviços independentes em **Python/FastAPI** (Produtos e Pagamentos).
- Banco de dados **PostgreSQL** para persistência.
- Arquitetura orientada a eventos simulada com **Observer Pattern**.
- Containerização com **Docker/Podman**.
- Orquestração com **Minikube (Kubernetes)**.
- Pipeline de **CI/CD com GitHub Actions**.
- Diagramas arquiteturais utilizando **C4 Model**.

# ShoopTree — Microserviços com FastAPI + PostgreSQL

Este projeto contém três serviços principais:
- **Banco de dados (Postgres)**
- **Serviço de Produtos (FastAPI)**
- **Serviço de Pagamentos (FastAPI)**

##  Rodando com Podman

### 1. Build das imagens
Na raiz do projeto:
```
podman build -t shoop-db:latest ./db
podman build -t produtos-service:latest ./produtos_service
podman build -t pagamentos-service:latest ./pagamentos_service

---
```
##  Instruções de Execução

### 1. Ambiente Local (Podman/Docker)
```
podman-compose up --build

```
Endpoints disponíveis:

Produtos:

``` 
http://localhost:8000/produtos

```
Pagamentos:

```
http://localhost:8001/pagamentos

```
Rodando com Podman Desktop
Abra o Podman Desktop.

Vá em Containers → Compose → Import Project.

Selecione o diretório do projeto (ShoopTree).

Clique em Run para iniciar os serviços.

Use o painel do Podman Desktop para visualizar logs e endpoints.

Rodando com Minikube
1. Iniciar cluster
```
minikube start --driver=docker
```
2. Carregar imagens locais
```
minikube image load shoop-db:latest
minikube image load produtos-service:latest
minikube image load pagamentos-service:latest
```
3. Aplicar manifests
```
kubectl apply -f k8s/deployment-db.yaml
kubectl apply -f k8s/service-db.yaml
kubectl apply -f k8s/deployment-produtos.yaml
kubectl apply -f k8s/service-produtos.yaml
kubectl apply -f k8s/deployment-pagamentos.yaml
kubectl apply -f k8s/service-pagamentos.yaml
```
4. Verificar pods e serviços
```
kubectl get pods
kubectl get svc
```
5. Acessar endpoints
```
minikube service produtos-service
minikube service pagamentos-service
```
 Testes de API
Produtos
Listar produtos

http
GET /produtos
Adicionar produto

http
POST /produtos
Body:
```
{
  "nome": "Notebook",
  "preco": 3500.00,
  "quantidade": 10
}
```
Pagamentos
Listar pagamentos

http
GET /pagamentos
Registrar pagamento

http
POST /pagamentos
Body:
```
{
  "produto_id": 1,
  "quantidade": 2,
  "valor": 7000.00
}
```
 Deployments e Services
Ver todos os deployments
```
kubectl get deployments
```
Ver todos os services
```
kubectl get svc
```
Ver detalhes de um deployment
```
kubectl describe deployment produtos-deployment
```
Ver detalhes de um service
```
kubectl describe svc produtos-service
```
Fluxo de validação
Criar produto via POST /produtos.

Listar produtos via GET /produtos.

Registrar pagamento via POST /pagamentos.

Conferir estoque atualizado.