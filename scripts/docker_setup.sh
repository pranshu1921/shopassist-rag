#!/bin/bash

# Docker Setup Script for ShopAssist RAG

set -e  # Exit on error

echo "======================================"
echo "ShopAssist RAG - Docker Setup"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it from .env.example"
    exit 1
fi

echo ""
echo "Step 1: Building Docker image..."
docker-compose build

echo ""
echo "Step 2: Setting up data (if not already done)..."

# Check if data exists
if [ ! -f "data/raw/products_50k.json" ]; then
    echo "  Downloading and processing data..."
    docker-compose run --rm shopassist-api python scripts/download_data.py
    docker-compose run --rm shopassist-api python scripts/generate_policies.py
    docker-compose run --rm shopassist-api python scripts/process_data.py
else
    echo "  ✓ Data already exists, skipping download"
fi

# Check if vector store exists
if [ ! -d "chroma_db/chroma.sqlite3" ]; then
    echo ""
    echo "Step 3: Building vector store..."
    docker-compose run --rm shopassist-api python scripts/build_vector_store.py
else
    echo "  ✓ Vector store already exists, skipping build"
fi

echo ""
echo "======================================"
echo "✓ Setup complete!"
echo "======================================"
echo ""
echo "To start the services:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the services:"
echo "  docker-compose down"
echo ""
echo "Access the application:"
echo "  API:  http://localhost:8000"
echo "  UI:   http://localhost:8501"
echo "  Docs: http://localhost:8000/docs"
echo ""