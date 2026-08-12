# MLOps — API de Predição de Imóveis

Projeto completo de **MLOps para servir um modelo de Machine Learning através de uma API REST**, com persistência das previsões, containerização e orquestração utilizando Kubernetes.

O projeto foi desenvolvido com foco em construir uma arquitetura de um ambiente real de produção, utilizando **Python, FastAPI, PostgreSQL, Docker e Kubernetes**, além de práticas como migrations, health checks, gerenciamento de recursos, escalabilidade automática e persistência de dados.

---

## Objetivo

Construir uma solução capaz de:

* Treinar e versionar um modelo de Machine Learning;
* Disponibilizar o modelo através de uma API REST;
* Receber características de um imóvel;
* Realizar uma previsão de preço;
* Armazenar as previsões no PostgreSQL;
* Executar migrations utilizando Alembic;
* Empacotar a aplicação com Docker;
* Executar a aplicação em Kubernetes;
* Escalar automaticamente a API utilizando HPA;
* Utilizar Ingress para expor a aplicação;
* Implementar health checks através de Kubernetes Probes;
* Persistir os dados do PostgreSQL através de Persistent Volumes;
* Executar testes automatizados.

---

# Arquitetura

```text
                         CLIENTE
                            │
                            │ HTTP
                            ▼
                  ┌───────────────────┐
                  │      Ingress      │
                  │   NGINX Ingress   │
                  │ api.mlops.local   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Kubernetes        │
                  │ Service           │
                  │ mlops-api-service │
                  └─────────┬─────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │      Deployment         │
              │        MLOps API        │
              │                          │
              │  ┌──────┐ ┌──────┐      │
              │  │ Pod  │ │ Pod  │ ...  │
              │  │ API  │ │ API  │      │
              │  └──────┘ └──────┘      │
              └────────────┬─────────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      ┌─────────────┐            ┌──────────────┐
      │ ML Model    │            │ PostgreSQL   │
      │ modelo.pkl  │            │              │
      └─────────────┘            └──────┬───────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ Persistent      │
                               │ Volume          │
                               └─────────────────┘

             Kubernetes HPA
                  │
                  ▼
       CPU / Memory Monitoring
                  │
                  ▼
       Aumenta ou reduz Pods
```

---

# Fluxo da aplicação

Uma requisição de previsão segue aproximadamente este fluxo:

```text
Cliente
   │
   │ POST /predict
   ▼
Ingress
   │
   ▼
Kubernetes Service
   │
   ▼
FastAPI Pod
   │
   ▼
Pydantic Validation
   │
   ▼
PredictionService
   │
   ├──────────────► Modelo ML
   │                    │
   │                    ▼
   │              Predição
   │
   ▼
PostgreSQL
   │
   ▼
Resposta JSON
```

---

# Machine Learning

O projeto possui uma estrutura separada para o ciclo de inferência do modelo:

```text
api/ml/
├── inference.py
├── model.py
├── postprocessing.py
├── preprocessing.py
└── validation.py
```

O modelo treinado é armazenado em:

```text
modelos/
└── v1/
    └── modelo.pkl
```

Essa organização permite separar responsabilidades entre:

* carregamento do modelo;
* pré-processamento;
* validação dos dados;
* inferência;
* pós-processamento.

O treinamento está separado da API:

```text
train/
└── train.py
```

Isso evita misturar o processo de treinamento com o processo de serving do modelo.

---

# API

A aplicação utiliza **FastAPI** para disponibilizar o modelo como serviço REST.

## Endpoints

### `GET /`

Verifica se a API está funcionando.

Resposta:

```json
{
  "mensagem": "API Funcionando",
  "status": "online"
}
```

---

### `GET /health`

Endpoint utilizado principalmente pelos Kubernetes Probes.

```json
{
  "status": "ok"
}
```

Esse endpoint é utilizado por:

* `startupProbe`
* `readinessProbe`
* `livenessProbe`

---

### `GET /info`

Retorna informações sobre o modelo e a aplicação.

```json
{
  "modelo": "Predição de imóveis",
  "versao": "1.0",
  "framework": "FastAPI"
}
```

---

### `GET /autor`

```json
{
  "autor": "Sam Souza"
}
```

---

### `GET /empresa`

```json
{
  "empresa": "Imobiliária X"
}
```

---

### `POST /predict`

Endpoint principal da aplicação.

Exemplo de entrada:

```json
{
  "area": 120,
  "quartos": 3,
  "banheiros": 2,
  "garagem": 2
}
```

O serviço processa os dados, executa o modelo e registra a previsão no banco de dados.

---

# Banco de dados

O projeto utiliza:

**PostgreSQL 17**

A aplicação utiliza SQLAlchemy para comunicação com o banco.

Estrutura relacionada ao banco:

```text
api/database/
├── connection.py
├── dependencies.py
├── init_db.py
├── models.py
├── session.py
├── repositories/
│   ├── prediction_repository.py
│   └── prediction_service.py
└── services/
    ├── main.py
    └── schemas.py
```

A aplicação utiliza o padrão de separação de responsabilidades entre:

```text
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Database
```

Isso facilita manutenção, testes e evolução da aplicação.

---

# Migrations

As alterações da estrutura do banco são controladas utilizando **Alembic**.

Estrutura:

```text
alembic/
├── env.py
├── script.py.mako
└── versions/
    └── e8336af6b56f_criando_tabela_previsoes.py
```

A migration pode ser executada através de:

```bash
alembic upgrade head
```

No Kubernetes, essa responsabilidade foi separada em um **Job**:

```text
migration-job.yaml
```

Assim, a criação/atualização da estrutura do banco não fica acoplada à inicialização da API.

---

# Docker

A aplicação possui um `Dockerfile` responsável por criar a imagem da API.

Build:

```bash
docker build -t mlops-api:v1 .
```

Executar:

```bash
docker run -p 8000:8000 mlops-api:v1
```

A aplicação pode ser acessada em:

```text
http://localhost:8000
```

A documentação automática do FastAPI está disponível em:

```text
http://localhost:8000/docs
```

---

# Docker Compose

Para desenvolvimento local, o projeto possui:

```text
docker-compose.yml
```

A arquitetura local contém dois serviços:

```text
┌──────────────────┐
│      API         │
│    FastAPI       │
│     :8000        │
└────────┬─────────┘
         │
         │ Docker Network
         │
┌────────▼─────────┐
│    PostgreSQL    │
│      :5432       │
└────────┬─────────┘
         │
         ▼
   postgres_data
```

Subir os serviços:

```bash
docker compose up --build
```

Executar em segundo plano:

```bash
docker compose up -d --build
```

Verificar os containers:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Parar:

```bash
docker compose down
```

---

# Kubernetes

O projeto também possui uma infraestrutura Kubernetes completa.

```text
k8s/
├── configmap.yaml
├── deployment.yaml
├── hpa.yaml
├── ingress.yaml
├── kind-config.yaml
├── migration-job.yaml
├── pod.yaml
├── postgres-deployment.yaml
├── postgres-pvc.yaml
├── postgres-service.yaml
├── pv.yaml
├── secret.yaml
└── service.yaml
```

---

# Deployment

A API é executada através de um Kubernetes Deployment:

```text
Deployment
    │
    ├── Pod
    ├── Pod
    └── Pod ...
```

O Deployment utiliza a imagem:

```text
samuelpa8x100/mlops-api:latest
```

Além disso, foram configurados limites de recursos:

```yaml
requests:
  cpu: "250m"
  memory: "256Mi"

limits:
  cpu: "500m"
  memory: "512Mi"
```

Isso permite ao Kubernetes saber quanto recurso a aplicação necessita e qual o limite máximo permitido.

---

# Health Checks

A aplicação utiliza três mecanismos de verificação:

## Startup Probe

Verifica se a aplicação conseguiu iniciar corretamente.

```text
startupProbe
     │
     ▼
GET /health
```

---

## Readiness Probe

Determina se o Pod está pronto para receber tráfego.

```text
Pod pronto?
   │
   ├── NÃO → não recebe tráfego
   │
   └── SIM → recebe tráfego
```

---

## Liveness Probe

Verifica se a aplicação continua funcionando.

```text
Aplicação saudável?
       │
       ├── SIM → continua
       │
       └── NÃO → Kubernetes reinicia o container
```

---

# Horizontal Pod Autoscaler

O projeto utiliza **HPA** para realizar escalabilidade automática.

Configuração:

```text
Minimum replicas: 1
Maximum replicas: 25
CPU target:       70%
Memory target:    80%
```

Fluxo:

```text
                 HPA
                  │
        ┌─────────┴─────────┐
        │                   │
     CPU > 70%          Memory > 80%
        │                   │
        └─────────┬─────────┘
                  ▼
             Mais Pods
```

Quando a carga aumenta, o Kubernetes pode aumentar a quantidade de Pods.

Quando a carga diminui, o Kubernetes pode reduzir a quantidade de Pods.

---

# Service

A API utiliza um Service do tipo:

```text
ClusterIP
```

O Service recebe tráfego na porta:

```text
80
```

e encaminha para:

```text
8000
```

Fluxo:

```text
Ingress
   │
   ▼
Service :80
   │
   ▼
Pod :8000
```

---

# Ingress

O acesso externo à API é realizado através de NGINX Ingress.

Host configurado:

```text
api.mlops.local
```

O fluxo é:

```text
localhost:80
      │
      ▼
NGINX Ingress
      │
      ▼
mlops-api-service:80
      │
      ▼
Pod:8000
```

O projeto utiliza **Kind** para executar o cluster Kubernetes localmente.

O `kind-config.yaml` realiza o mapeamento:

```text
Host :80
   │
   ▼
Kind Node :80
   │
   ▼
Ingress Controller
```

---

# Persistência do PostgreSQL

O PostgreSQL utiliza:

```text
PersistentVolume
        │
        ▼
PersistentVolumeClaim
        │
        ▼
PostgreSQL Pod
```

Arquivos relacionados:

```text
pv.yaml
postgres-pvc.yaml
```

O volume utiliza:

```text
ReadWriteOnce
```

e possui capacidade configurada de:

```text
5Gi
```

Enquanto o PVC solicita:

```text
1Gi
```

O objetivo é evitar que os dados do PostgreSQL desapareçam simplesmente porque o Pod foi recriado.

---

# Configuração e Secrets

As configurações não relacionadas a credenciais são armazenadas em:

```text
ConfigMap
```

Exemplo:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
MODEL_VERSION
```

As credenciais ficam em:

```text
Secret
```

Exemplo:

```text
DB_PASSWORD
DB_USER
DB_NAME
```

A aplicação recebe essas configurações através de:

```yaml
envFrom:
  - configMapRef:
      name: mlops-config

  - secretRef:
      name: mlops-secret
```

> Em um ambiente real de produção, secrets não devem ser versionados no Git dessa forma. O ideal é utilizar um gerenciador de secrets, como AWS Secrets Manager, Kubernetes Secrets integrado a uma solução de gerenciamento ou outro mecanismo apropriado.

---

# Testes

O projeto possui testes automatizados:

```text
tests/
├── conftest.py
├── test_api.py
├── test_model.py
├── test_prediction_service.py
├── test_repository.py
└── test_validation.py
```

Os testes cobrem diferentes camadas da aplicação:

```text
API
 │
 ├── Model
 │
 ├── Validation
 │
 ├── Prediction Service
 │
 └── Repository
```

Para executar:

```bash
pytest
```

---

# Estrutura do projeto

```text
mlops-engineer/
│
├── api/
│   ├── config/
│   ├── database/
│   ├── ml/
│   ├── services/
│   ├── main.py
│   └── schemas.py
│
├── alembic/
│   └── versions/
│
├── dados/
│   └── dados_imoveis.csv
│
├── modelos/
│   └── v1/
│       └── modelo.pkl
│
├── train/
│   └── train.py
│
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   ├── test_prediction_service.py
│   ├── test_repository.py
│   └── test_validation.py
│
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── kind-config.yaml
│   ├── migration-job.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-service.yaml
│   ├── pv.yaml
│   ├── secret.yaml
│   └── service.yaml
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── treino.py
```

---

# Executando localmente

## 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
cd mlops-engineer
```

## 2. Criar ambiente virtual

```bash
python3 -m venv .venv
```

Ativar:

```bash
source .venv/bin/activate
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar variáveis de ambiente

Criar um arquivo:

```text
.env
```

Exemplo:

```env
APP_PORT=8000

DB_HOST=postgres
DB_PORT=5432
DB_USER=sam
DB_PASSWORD=123456
DB_NAME=mlops
```

> Para produção, utilize secrets apropriados em vez de armazenar senhas diretamente em arquivos de configuração.

---

# Executando com Docker Compose

```bash
docker compose up --build
```

Depois acesse:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# Executando com Kubernetes

O cluster foi desenvolvido utilizando **Kind**.

Criar o cluster:

```bash
kind create cluster --name mlops --config k8s/kind-config.yaml
```

Verificar:

```bash
kubectl get nodes
```

---

## Criar configurações

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

---

## Criar PostgreSQL

```bash
kubectl apply -f k8s/pv.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

Verificar:

```bash
kubectl get pods
```

---

## Executar migration

```bash
kubectl apply -f k8s/migration-job.yaml
```

Verificar:

```bash
kubectl get jobs
```

Logs:

```bash
kubectl logs job/mlops-db-migradtion
```

---

## Criar API

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Verificar:

```bash
kubectl get pods
kubectl get services
```

---

## Criar HPA

```bash
kubectl apply -f k8s/hpa.yaml
```

Verificar:

```bash
kubectl get hpa
```

Exemplo:

```text
NAME            REFERENCE              TARGETS
mlops-api-hpa   Deployment/mlops-api   cpu: 70%/70%
```

---

## Configurar Ingress

```bash
kubectl apply -f k8s/ingress.yaml
```

Verificar:

```bash
kubectl get ingress
```

O host utilizado é:

```text
api.mlops.local
```

Para acessar localmente, o domínio deve apontar para:

```text
127.0.0.1
```

Por exemplo, no arquivo `/etc/hosts`:

```text
127.0.0.1 api.mlops.local
```

Depois:

```bash
curl http://api.mlops.local/
```

---

# Observabilidade

A arquitetura foi preparada para receber ferramentas de observabilidade posteriormente.

A evolução planejada inclui:

```text
Prometheus
    │
    ▼
Métricas
    │
    ▼
Grafana
```

Entre as métricas importantes estão:

* CPU;
* memória;
* quantidade de Pods;
* latência;
* quantidade de requisições;
* erros HTTP;
* utilização da API;
* métricas relacionadas ao modelo.

---

# Pipeline MLOps

A arquitetura do projeto pode evoluir para o seguinte fluxo:

```text
Dados
  │
  ▼
Treinamento
  │
  ▼
Validação do Modelo
  │
  ▼
Versionamento
  │
  ▼
Docker
  │
  ▼
GitHub
  │
  ▼
CI/CD
  │
  ▼
Kubernetes
  │
  ▼
API de Predição
  │
  ▼
Monitoramento
```

---

# Tecnologias utilizadas

| Tecnologia        | Utilização                |
| ----------------- | ------------------------- |
| Python            | Linguagem principal       |
| FastAPI           | API REST                  |
| Pydantic          | Validação dos dados       |
| Scikit-learn      | Machine Learning          |
| Pandas            | Manipulação de dados      |
| SQLAlchemy        | ORM                       |
| PostgreSQL        | Banco de dados            |
| Alembic           | Database migrations       |
| Pytest            | Testes                    |
| Docker            | Containerização           |
| Docker Compose    | Ambiente local            |
| Kubernetes        | Orquestração              |
| Kind              | Kubernetes local          |
| NGINX Ingress     | Exposição da API          |
| HPA               | Escalabilidade automática |
| PersistentVolume  | Persistência              |
| ConfigMap         | Configuração              |
| Kubernetes Secret | Credenciais               |

---

# Conceitos de MLOps aplicados

Este projeto aplica conceitos importantes de engenharia de Machine Learning:

### Machine Learning Serving

O modelo deixa de ser apenas um arquivo utilizado em um notebook e passa a ser disponibilizado como um serviço.

### API

O modelo é consumido através de uma interface REST.

### Containerização

A aplicação é empacotada em uma imagem Docker reproduzível.

### Database

As previsões podem ser persistidas em PostgreSQL.

### Database Migration

Alterações do banco são controladas pelo Alembic.

### Orquestração

O Kubernetes gerencia os containers da aplicação.

### Health Checks

A aplicação possui mecanismos para verificar disponibilidade e saúde.

### Auto Scaling

O HPA permite aumentar ou reduzir a quantidade de Pods conforme utilização de recursos.

### Persistence

O PostgreSQL possui armazenamento persistente.

### Configuration Management

Configurações e credenciais são separadas da aplicação através de ConfigMap e Secret.

### Testing

A aplicação possui testes separados por camada.

---

# Próximas evoluções

A arquitetura foi construída pensando em uma evolução para um ambiente MLOps mais completo.

Próximos passos:

* [ ] GitHub Actions
* [ ] CI/CD
* [ ] AWS
* [ ] ECR
* [ ] EKS
* [ ] MLflow
* [ ] Airflow
* [ ] Prometheus
* [ ] Grafana
* [ ] Monitoramento de drift
* [ ] Monitoramento de performance do modelo
* [ ] Versionamento automatizado de modelos
* [ ] Deploy automatizado
* [ ] RAG / LLM

---

# Autor

**Samuel Souza**

Projeto desenvolvido como parte da construção de conhecimentos práticos em:

**MLOps • Machine Learning • Data Engineering • Python • APIs • Docker • Kubernetes • Cloud**

---

# Sobre o projeto

Este projeto foi desenvolvido com o objetivo de demonstrar, de ponta a ponta, como transformar um modelo de Machine Learning em uma aplicação que pode ser **testada, containerizada, implantada, escalada e monitorada**, aproximando o desenvolvimento de ML das práticas utilizadas em engenharia de software e infraestrutura.

---
