# ShoopTree — Prova de Conceito

##  Objetivo
Este projeto é uma prova de conceito funcional que demonstra:
- Arquitetura de **microserviços** independentes em **Python/FastAPI**.
- Banco de dados **PostgreSQL** para persistência.
- Comunicação orientada a eventos simulada com **Observer Pattern**.
- Containerização com **Docker/Podman**.
- Orquestração com **Minikube (Kubernetes)**.
- Pipeline de **CI/CD com GitHub Actions**.
- Diagramas arquiteturais utilizando **C4 Model**:
  - Diagrama de Contexto
  - Diagrama de Containers

---

##  Serviços Implementados

### Serviço de Produtos
- **GET /produtos** → lista todos os produtos cadastrados.
- **POST /produtos** → adiciona um novo produto com nome, preço e quantidade.

### Serviço de Pagamentos
- **GET /pagamentos** → lista todos os pagamentos registrados.
- **POST /pagamentos** → registra um pagamento associado a um produto.

### Shoop API Gateway
- **POST /compras** → cria uma compra e publica um evento no barramento.
- **GET /eventos** → retorna o histórico de eventos publicados.

---

##  Evento Simulado
A arquitetura orientada a eventos foi implementada com classes Python representando **Producer** e **Consumer**, sem uso de Kafka ou ferramentas externas.

Fluxo:
1. O endpoint `/compras` gera um evento do tipo **COMPRA**.
2. O **PagamentoConsumer** consome o evento e processa o pagamento.
3. O **NotificacaoConsumer** consome o evento e envia uma notificação.
4. O histórico de eventos pode ser consultado em `/eventos`.

---

##  Design Pattern Utilizado
Foi aplicado o **Observer Pattern**:
- O **EventBus** atua como sujeito (publisher).
- Os consumidores (`PagamentoConsumer`, `NotificacaoConsumer`) atuam como observadores.
- Quando um evento é publicado, todos os observadores inscritos são notificados automaticamente.

 Justificativa: O Observer Pattern é ideal para simular uma arquitetura orientada a eventos, pois desacopla produtores e consumidores, permitindo que múltiplos serviços reajam a um mesmo evento sem dependência direta.

---
##  Descrição da Arquitetura
A arquitetura da ShoopTree foi modernizada para sair do modelo monolítico e adotar microserviços independentes:
- **Shoop API Gateway** centraliza requisições e publica eventos.
- **Serviço de Produtos** gerencia catálogo e estoque.
- **Serviço de Pagamentos** processa transações financeiras.
- **EventBus (Observer Pattern)** simula comunicação orientada a eventos.
- **Consumidores** (PagamentoConsumer e NotificacaoConsumer) reagem aos eventos de compra.
- **Banco de Dados PostgreSQL** garante persistência dos dados.

Essa arquitetura melhora escalabilidade, isolamento de falhas e clareza de responsabilidades.
---
Instruções de Execução
1. Ambiente Local (Podman/Docker)
Logar no Docker Hub:

bash
podman login docker.io
Subir o Compose:

bash
podman-compose up --build
Endpoints disponíveis:

Produtos → http://localhost:8000/produtos

Pagamentos → http://localhost:8001/pagamentos

Shoop API → http://localhost:8080/compras e http://localhost:8080/eventos

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
minikube image load shoop-api:latest
```
3. Aplicar manifests
```
kubectl apply -f k8s/deployment-db.yaml
kubectl apply -f k8s/service-db.yaml
kubectl apply -f k8s/deployment-produtos.yaml
kubectl apply -f k8s/service-produtos.yaml
kubectl apply -f k8s/deployment-pagamentos.yaml
kubectl apply -f k8s/service-pagamentos.yaml
kubectl apply -f k8s/deployment-shoop-api.yaml
kubectl apply -f k8s/service-shoop-api.yaml
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
minikube service shoop-api
```
 Testes de API
Shoop API Gateway
Criar compra

Código
POST /compras?produto_id=1&quantidade=2
Resposta esperada:

json
```
{
  "status": "Compra registrada",
  "evento": {
    "tipo": "COMPRA",
    "produto_id": 1,
    "quantidade": 2
  }
}
```
Listar eventos

Código
GET /eventos
Retorna o histórico de eventos publicados.

Produtos
Listar produtos

Código
GET /produtos
Adicionar produto

json
POST /produtos
```
{
  "nome": "Notebook",
  "preco": 3500.00,
  "quantidade": 10
}
```
Pagamentos
Listar pagamentos

Código
GET /pagamentos
Registrar pagamento

json
POST /pagamentos
```
{
  "produto_id": 1,
  "quantidade": 2,
  "valor": 7000.00
}
```
 Deployments e Services
Ver todos os deployments:

```
kubectl get deployments
```
Ver todos os services:

```
kubectl get svc
```
Ver detalhes de um deployment:

```
kubectl describe deployment shoop-api-deployment
```
Ver detalhes de um service:

```
kubectl describe svc shoop-api
```
 Fluxo de Validação
Criar produto via POST /produtos.

Listar produtos via GET /produtos.

Registrar compra via POST /compras.

Conferir histórico via GET /eventos.

Ver consumidores reagindo nos logs do pod da Shoop API.

 Estrutura do Projeto
Código
```
ShoopTree/
├── shoop_api/
│   └── main.py
├── simulacao_eventos/
│   └── event_bus.py
├── produtos_service/
├── pagamentos_service/
├── db/
├── k8s/
│   ├── deployment-*.yaml
│   └── service-*.yaml
└── Dockerfile
```
