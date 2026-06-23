#  Autism Chat Bot — Docker Setup

A production-ready RAG-based chatbot for Autism support, powered by FastAPI, MongoDB, Qdrant, and a full monitoring stack.

---

##  Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Services & URLs](#services--urls)
- [Database Restore](#database-restore)
- [Monitoring Setup](#monitoring-setup)
- [Troubleshooting](#troubleshooting)

---

##  Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) v24+
- [Docker Compose](https://docs.docker.com/compose/) v2+
- Minimum **8GB RAM** recommended
- Minimum **10GB free disk space**

---

##  Project Structure

```
docker/
├── autism_chat_bot/
│   └── Dockerfile                  # FastAPI app Docker image
├── env/
│   ├── .env.app                    # FastAPI environment variables
│   ├── .env.example.app            # FastAPI env template (copy this)
│   ├── .env.grafana                # Grafana environment variables
│   └── .env.grafana.example        # Grafana env template (copy this)
├── mongodb/                        # MongoDB config (if any)
├── nginx/
│   └── default.conf                # Nginx reverse proxy config
├── prometheus.yml/
│   └── promethues.yml              # Prometheus scrape config
├── backup/
│   ├── Autism_chat_bot/            # MongoDB dump
│   └── qdrant_backup.tar.gz        # Qdrant vector backup
├── .env                            # Root env file
├── .env.example                    # Root env template
├── .gitignore
└── docker-compose.yml              # Main Docker Compose file
```

---

##  Services Overview

| Service | Image | Description |
|---|---|---|
| **FastAPI** | Custom build | Main chatbot API |
| **MongoDB** | mongo:7-jammy | Primary database |
| **Qdrant** | qdrant/qdrant:v1.13.6 | Vector database for RAG |
| **Nginx** | nginx:stable-alpine | Reverse proxy |
| **Prometheus** | prom/prometheus:v3.3.0 | Metrics collection |
| **Grafana** | grafana/grafana:11.6.0-ubuntu | Monitoring dashboards |
| **Node Exporter** | prom/node-exporter:v1.9.1 | System metrics |

---

##  Environment Variables

### Step 1 — Copy the example files

```bash
cp env/.env.example.app env/.env.app
cp env/.env.grafana.example env/.env.grafana
```

### Step 2 — Fill in the values

#### `env/.env.app` — FastAPI Configuration

| Variable | Description | Example |
|---|---|---|
| `APP_NAME` | Application name | `autism_chat_bot` |
| `APP_VERSION` | Application version | `0.1` |
| `FILE_ALLOWED_EXTENSION` | Allowed upload file types | `["text/plain","application/pdf","application/epub+zip"]` |
| `CHUNK_SIZE` | File chunk size in bytes | `512000` |
| `MONGO_URL` | MongoDB connection string | `mongodb://mongodb:27017` |
| `MONGO_DATABASE` | MongoDB database name | `Autism_chat_bot` |
| `GENERATION_BACK_END` | LLM backend provider | `COHERE` or `OPENAI` |
| `EMBEDDING_BACK_END` | Embedding backend provider | `COHERE` or `OPENAI` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | `sk-...` |
| `OPEN_API_URL` | OpenAI base URL | `https://api.openai.com` |
| `COHERE_API_KEY` | Cohere API key (if using Cohere) | `...` |
| `GENERATION_MODEL_ID` | LLM model to use | `command-a-03-2025` |
| `EMBEDDING_MODEL_ID` | Embedding model to use | `embed-multilingual-v3.0` |
| `EMBEDDING_MODEL_SIZE` | Embedding vector dimensions | `1024` |
| `GENERATION_DEFAULT_MAX_TOKENS` | Max tokens per response | `1000` |
| `INPUT_DEFAULT_MAX_CHARACTERS` | Max input characters | `1024` |
| `GENERATION_DEFAULT_MAX_CHARACTERS` | Max output characters | `1024` |
| `TEMPRETURE` | LLM temperature (0.0 - 1.0) | `0.5` |
| `QDRANT_HOST` | Qdrant server host | `qdrant` |
| `QDRANT_PORT` | Qdrant server port | `6333` |
| `VECTOR_DB_BACKEND` | Vector DB provider | `QDRANT` |
| `VECTOR_DB_DISTANCE_METHOD` | Vector similarity method | `cosine` |
| `DEFAULT_LANGUAGE` | Default response language | `english` |
| `LANGUAGE` | Active language | `english` |

>  **Important:** `MONGO_URL` must use `mongodb://mongodb:27017` (container name, not localhost)

>  **Important:** `QDRANT_HOST` must be `qdrant` (container name, not localhost)

#### `env/.env.grafana` — Grafana Configuration

| Variable | Description | Example |
|---|---|---|
| `GF_SECURITY_ADMIN_USER` | Grafana admin username | `admin` |
| `GF_SECURITY_ADMIN_PASSWORD` | Grafana admin password | `strongpassword` |
| `GF_USERS_ALLOW_SIGN_UP` | Allow new user registration | `false` |

---

##  Running the Project

### Step 1 — Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>/docker
```

### Step 2 — Set up environment variables

```bash
cp env/.env.example.app env/.env.app
cp env/.env.grafana.example env/.env.grafana
```

Fill in the required values in both files (especially the API keys).

### Step 3 — Start all services

```bash
docker compose up -d
```

This will start all 7 services automatically in the correct order.

### Step 4 — Verify all services are running

```bash
docker compose ps
```

All services should show `running` or `healthy` status.

---

##  Services & URLs

| Service | URL | Credentials |
|---|---|---|
| **FastAPI** | http://localhost:8000 | — |
| **Swagger UI** | http://localhost:8000/docs | — |
| **Nginx** | http://localhost:80 | — |
| **MongoDB** | localhost:27007 | No auth (dev mode) |
| **Qdrant Dashboard** | http://localhost:6333/dashboard | — |
| **Prometheus** | http://localhost:9090 | — |
| **Grafana** | http://localhost:3000 | Set in `.env.grafana` |
| **Node Exporter** | http://localhost:9100 | — |

---

##  Database Restore

After starting the services, restore the databases from the backup:

### MongoDB Restore

```bash
# Copy backup into the container
docker cp ./backup/Autism_chat_bot mongodb:/data/db/backup/Autism_chat_bot

# Restore the database
docker exec mongodb mongorestore /data/db/backup
```

### Qdrant Restore

```bash
# Copy backup into the container
docker cp ./backup/qdrant_backup.tar.gz qdrant:/tmp/qdrant_backup.tar.gz

# Extract the backup
docker exec qdrant tar -xzf /tmp/qdrant_backup.tar.gz -C /

# Restart Qdrant to load the data
docker restart qdrant
```

### Verify Restore

```bash
# Check MongoDB
docker exec mongodb mongosh --eval "db.adminCommand('listDatabases')"

# Check Qdrant collections
curl http://localhost:6333/collections
```

---

##  Monitoring Setup

### Step 1 — Open Grafana

Go to http://localhost:3000 and login with credentials from `.env.grafana`

### Step 2 — Add Prometheus Data Source

1. Go to **Connections** → **Data Sources** → **Add data source**
2. Select **Prometheus**
3. Set URL to: `http://prometheus:9090`
4. Click **Save & Test**

### Step 3 — Import Dashboards

Go to **Dashboards** → **Import** and use these IDs:

| Dashboard | ID | Description |
|---|---|---|
| Node Exporter | `1860` | CPU, Memory, Disk, Network |
| FastAPI | `22676` | API requests, latency, errors |
| Qdrant | `25152` | Vector DB operations |

---

##  Re-index Vectors (if needed)

If Qdrant is empty and you need to re-generate embeddings from existing MongoDB data:

```bash
curl -X POST http://localhost:8000/nlp/index/push/books_chunks \
  -H "Content-Type: application/json" \
  -d '{"do_reset": 1}'
```

>  This process takes several minutes depending on the amount of data.

---

##  Stopping the Project

```bash
# Stop all services (data is preserved)
docker compose down

# Stop and remove all data (CAUTION: this deletes everything)
docker compose down -v
```

---

##  Troubleshooting

### Check logs for a specific service

```bash
docker compose logs <service-name> --tail=50

# Examples:
docker compose logs fastapi --tail=50
docker compose logs mongodb --tail=20
docker compose logs qdrant --tail=20
```

### FastAPI not starting?

```bash
# Check if MongoDB is healthy first
docker compose ps mongodb

# Rebuild FastAPI image
docker compose up -d --build fastapi
```

### Qdrant collections empty?

```bash
# Verify collections exist
curl http://localhost:6333/collections

# If empty, re-run the indexing endpoint
curl -X POST http://localhost:8000/nlp/index/push/books_chunks \
  -H "Content-Type: application/json" \
  -d '{"do_reset": 1}'
```

### Reset everything and start fresh

```bash
docker compose down -v
docker compose up -d
```

---

##  Tech Stack

| Layer | Technology |
|---|---|
| **API** | FastAPI + Python 3.11 |
| **Architecture** | Clean Architecture |
| **Primary DB** | MongoDB 7 |
| **Vector DB** | Qdrant v1.13.6 |
| **LLM** | Cohere / OpenAI |
| **Reverse Proxy** | Nginx |
| **Monitoring** | Prometheus + Grafana |
| **Containerization** | Docker + Docker Compose |