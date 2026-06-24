```markdown
# Autism Chat Bot 🧩

![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-ready-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-teal)
![LangChain](https://img.shields.io/badge/LangChain-1.2.12-orange)

An AI-powered chatbot and document processing system designed to assist with autism-related knowledge retrieval.  
It uses **FastAPI**, **LangChain**, and **LLM providers (OpenAI, Cohere)** with **Qdrant Vector DB** and **MongoDB** for semantic search and RAG-based answers.  
Deployment is fully containerized with **Docker Compose**, including monitoring via **Prometheus + Grafana**.

---

##  Quickstart

```bash
# Clone the repository
git clone https://github.com/username/autism_chat_bot.git
cd autism_chat_bot

# Install dependencies
pip install -r src/requirments.txt

# Run locally
uvicorn src.routes.main:app --reload
```

Open the API docs at:
```
http://localhost:8000/docs
```

---

##  Features
-  Upload and index books & papers related to Autism Spectrum Disorder (ASD).
-  Semantic search powered by **Qdrant** vector database.
-  LLM integration with **OpenAI** and **Cohere**.
-  Retrieval-Augmented Generation (RAG) answers from indexed documents.
-  Fast and scalable API using **FastAPI + Uvicorn**.
-  Monitoring and metrics via **Prometheus, Grafana, Node Exporter**.
-  Health checks with **FastAPI Health**.
-  Reverse proxy with **Nginx**.

---

##  Configuration

The application can be customized via environment variables or `config.py`:

- `APP_NAME` → Application name  
- `APP_VERSION` → Version number  
- `FILE_ALLOWED_EXTENSION` → Supported file types (PDF, EPUB, TXT)  
- `CHUNK_SIZE` → Default chunk size for file splitting  
- `GENERATION_BACK_END` → LLM provider (OpenAI or Cohere)  
- `GENERATION_MODEL_ID` → Model ID (e.g., `command-a-03-2025`)  
- `EMBEDDING_MODEL_ID` → Embedding model (e.g., `embed-multilingual-v3.0`)  
- `VECTOR_DB_BACKEND` → Vector DB (Qdrant)  
- `LANGUAGE` → Default language (English/Arabic)  

---

##  Project Structure
```
Autism_Chat_bot/
├── docker/              # Docker setup (compose, configs, backups)
├── src/
│   ├── assets/          # Books, papers, vector DB data
│   ├── controllers/     # Data and NLP controllers
│   ├── helpers/         # Config and utilities
│   ├── models/          # Database schemas and enums
│   ├── routes/          # FastAPI routes (main entry point)
│   ├── repository/      # Database repositories and data access layer
│   ├── stores/          # LLM + Vector DB providers
│   └── utilies/         # Metrics and utilities
├── LICENSE              # License file
└── README.md            # Documentation
```

---

##  API Endpoints

###  Upload a file
```http
POST /upload/{category_id}
```

###  Bulk upload
```http
POST /bulk_upload/{category_id}
```

###  Process file into chunks
```http
POST /file_process/{category_id}/chunks
```

###  Index chunks into Vector DB
```http
POST /nlp/index/push/{category_id}
```

###  Get Vector DB info
```http
GET /nlp/get_info/{category_id}
```

###  Semantic search
```http
POST /nlp/search/{category_id}
```

###  Answer with RAG
```http
POST /nlp/answer/{category_id}
```

---

##  Usage Examples

### Upload a single file
```bash
curl -X POST "http://localhost:8000/upload/books" \
  -F "file=@book.pdf" \
  -F 'data={"title":"Example Book","authors":["Author Name"],"year":2025}'
```

### Bulk upload multiple files
```bash
curl -X POST "http://localhost:8000/bulk_upload/papers" \
  -F "files=@paper1.pdf" \
  -F "files=@paper2.pdf" \
  -F 'data=[{"title":"Paper 1","authors":["Author A"],"year":2024},{"title":"Paper 2","authors":["Author B"],"year":2023}]'
```

### Process file into chunks
```bash
curl -X POST "http://localhost:8000/file_process/books/chunks" \
  -F "file=@book.pdf" \
  -F "chunk_size=512000" \
  -F "over_lap=100"
```

### Search in indexed data
```bash
curl -X POST "http://localhost:8000/nlp/search/books" \
  -H "Content-Type: application/json" \
  -d '{"text":"What are common autism symptoms?","limit":5}'
```

### Get AI Answer (RAG)
```bash
curl -X POST "http://localhost:8000/nlp/answer/books" \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain autism spectrum disorder","limit":3}'
```

---

##  Docker Deployment

```bash
docker-compose up --build
```

### Services
- **FastAPI** → `http://localhost:8000`
- **Nginx Reverse Proxy** → `http://localhost:80`
- **MongoDB** → `localhost:27007`
- **Qdrant Vector DB** → `http://localhost:6333`
- **Prometheus** → `http://localhost:9090`
- **Grafana** → `http://localhost:3000`
- **Node Exporter** → `http://localhost:9100`

---

##  Monitoring
- Prometheus metrics exposed at `/metrics`.
- Grafana dashboards available at `http://localhost:3000`.
- Node Exporter system metrics at `http://localhost:9100`.
- Health checks available at `/health`, `/health/live`, `/health/ready`.

---

##  Architecture Overview

```
[ FastAPI ] ---> [ MongoDB ] 
       |         [ Qdrant Vector DB ]
       |----> [ LLM Providers: OpenAI, Cohere ]
       |----> [ Prometheus + Grafana Monitoring ]
       |----> [ Nginx Reverse Proxy ]
```

---

##  Contributing
Contributions are welcome!  
Please fork the repository and submit a pull request.

---

##  License
This project is licensed under the MIT License.  
See the LICENSE file for details.
```

---
