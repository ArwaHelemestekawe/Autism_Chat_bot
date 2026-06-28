cat > team-share/README.txt << 'EOF'
===========================================
  AUTISM CHATBOT - TEAM SETUP GUIDE
===========================================

REQUIREMENTS:
  - Install Docker Desktop → https://www.docker.com/products/docker-desktop
  - Make sure Docker is running before you start

SETUP (run once):
  1. Open terminal inside this folder
  2. Load the Docker image:
     docker load -i docker-fastapi.tar

RUN:
  docker compose up -d

STOP:
  docker compose down

===========================================
  TEST THE API ENDPOINTS
===========================================

  Swagger UI  → http://localhost/docs
  API Base    → http://localhost/
  Qdrant DB   → http://localhost:6333/dashboard
  Grafana     → http://localhost:3000  (user: arwa / pass: arwa)
  Prometheus  → http://localhost:9090

===========================================
  TROUBLESHOOTING
===========================================

  Check if containers are running:
    docker compose ps

  Check logs if something is wrong:
    docker compose logs fastapi
    docker compose logs mongodb

EOF