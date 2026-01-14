# Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed
- Docker Compose installed
- `.env` file with OpenAI API key

### Option 1: Using Docker Compose (Recommended)
```bash
# 1. Setup (one-time)
bash scripts/docker_setup.sh

# 2. Start services
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop services
docker-compose down
```

### Option 2: Using Makefile
```bash
# Setup
make setup

# Build Docker image
make docker-build

# Start services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

### Option 3: Manual Docker Commands
```bash
# Build image
docker build -t shopassist-rag .

# Run API
docker run -d \
  --name shopassist-api \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/chroma_db:/app/chroma_db \
  shopassist-rag

# Run UI
docker run -d \
  --name shopassist-ui \
  -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/chroma_db:/app/chroma_db \
  shopassist-rag \
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## Services

### API Service
- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **Docs**: http://localhost:8000/docs

### UI Service
- **Port**: 8501
- **URL**: http://localhost:8501

## Data Persistence

Data is stored in Docker volumes:
- `data/` - Product and review data
- `chroma_db/` - Vector store
- `.cache/` - Response cache
- `logs/` - Application logs

## Testing Docker Deployment
```bash
# Run test script
bash scripts/docker_test.sh

# Or manually test
curl http://localhost:8000/health
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Out of memory
```bash
# Increase Docker memory limit (Docker Desktop)
# Settings → Resources → Memory → 8GB+
```

### API key not working
```bash
# Check .env file exists
ls -la .env

# Verify environment variable
docker-compose exec shopassist-api env | grep OPENAI
```

## Production Deployment

For production use:

1. **Use proper secrets management**
   - AWS Secrets Manager
   - Google Secret Manager
   - HashiCorp Vault

2. **Add reverse proxy**
   - Nginx
   - Traefik
   - AWS ALB

3. **Enable HTTPS**
   - Let's Encrypt
   - AWS Certificate Manager

4. **Add monitoring**
   - Prometheus + Grafana
   - CloudWatch
   - Datadog

5. **Configure scaling**
   - Docker Swarm
   - Kubernetes
   - ECS/EKS

## Resource Requirements

### Minimum
- 2 CPU cores
- 4GB RAM
- 10GB disk

### Recommended
- 4 CPU cores
- 8GB RAM
- 20GB disk