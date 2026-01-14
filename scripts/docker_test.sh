#!/bin/bash

# Test Docker deployment

echo "======================================"
echo "Testing ShopAssist RAG Docker Deployment"
echo "======================================"

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Test API health
echo ""
echo "Testing API health endpoint..."
API_HEALTH=$(curl -s http://localhost:8000/health)
echo "Response: $API_HEALTH"

# Test API query
echo ""
echo "Testing API query endpoint..."
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the best laptop for students?",
    "return_sources": false
  }' | python -m json.tool

echo ""
echo ""
echo "======================================"
echo "✓ Docker deployment test complete!"
echo "======================================"
echo ""
echo "Access the application:"
echo "  API:  http://localhost:8000"
echo "  UI:   http://localhost:8501"
echo "  Docs: http://localhost:8000/docs"