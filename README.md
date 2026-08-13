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

---

##  Instruções de Execução

### 1. Ambiente Local (Podman/Docker)
```bash
podman-compose up --build
Endpoints disponíveis:

Produtos: http://localhost:8000/produtos

Pagamentos: http://localhost:8001/pagamentos

2. Kubernetes (Minikube)
bash
minikube start --driver=podman
kubectl apply -f k8s/
kubectl get pods
kubectl get services
Acesse os serviços via:

bash
minikube service produtos-service
minikube service pagamentos-service
Arquitetura
Diagrama de Contexto
[Parece que o resultado não era seguro para exibição. Vamos mudar as coisas e tentar outra opção!]

Diagrama de Containers
[Parece que o resultado não era seguro para exibição. Vamos mudar as coisas e tentar outra opção!]

Serviços
Produtos Service
GET /produtos → lista produtos.

POST /produtos → adiciona novo produto.

Pagamentos Service
GET /pagamentos → lista pagamentos.

POST /pagamentos → registra pagamento e dispara eventos:

Notificação por email (simulada).

Atualização de estoque (simulada).

vento Simulado
A arquitetura orientada a eventos foi implementada com o Observer Pattern:

Um pagamento gera um evento.

Observadores reagem automaticamente:

notificar_email()

atualizar_estoque()

Design Pattern Utilizado
Foi aplicado o Observer Pattern, pois:

Permite que múltiplos componentes reajam a um evento sem acoplamento direto.

Facilita a extensão futura (novos observadores podem ser adicionados sem alterar o core).

Representa bem cenários reais de sistemas orientados a eventos.

CI/CD
Pipeline configurado em GitHub Actions:

Build das imagens com Podman.

Testes básicos de endpoints.

Execução automática em cada push/pull request para main.

Arquivo: .github/workflows/ci.yml

Tecnologias Utilizadas
Python 3.12 + FastAPI

PostgreSQL 16

Podman/Docker

Minikube + Kubernetes

GitHub Actions

C4 Model (Structurizr/Draw.io)

Autor
Projeto desenvolvido por Marco, como prova de conceito para disciplina de Arquitetura de Software.