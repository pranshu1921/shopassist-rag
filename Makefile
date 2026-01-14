# Makefile for ShopAssist RAG

.PHONY: help install setup data vector-store run-api run-ui test clean docker-build docker-up docker-down

help:
	@echo "ShopAssist RAG - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make setup         - Complete setup (install + data + vector-store)"
	@echo "  make data          - Download and process data"
	@echo "  make vector-store  - Build vector store"
	@echo ""
	@echo "Run:"
	@echo "  make run-api       - Start FastAPI server"
	@echo "  make run-ui        - Start Streamlit UI"
	@echo ""
	@echo "Test:"
	@echo "  make test          - Run evaluation tests"
	@echo "  make benchmark     - Run performance benchmark"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker services"
	@echo "  make docker-down   - Stop Docker services"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""
	@echo "Utility:"
	@echo "  make clean         - Clean cache and temporary files"

install:
	pip install -r requirements.txt

data:
	python scripts/download_data.py
	python scripts/generate_policies.py
	python scripts/process_data.py

vector-store:
	python scripts/build_vector_store.py

setup: install data vector-store
	@echo "✓ Setup complete!"

run-api:
	python src/api.py

run-ui:
	streamlit run app.py

test:
	python tests/test_queries.py

benchmark:
	python scripts/benchmark.py

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	rm -rf .cache/*
	rm -rf logs/*
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete