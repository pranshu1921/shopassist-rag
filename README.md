# ShopAssist RAG: AI-Powered E-Commerce Product Assistant

An intelligent shopping assistant that answers customer questions by retrieving information from product catalogs, customer reviews, and store policies.

## Project Status
🚧 Under Development

## Tech Stack
- LangChain for RAG orchestration
- ChromaDB for vector storage
- OpenAI for embeddings and LLM
- FastAPI for backend API
- Streamlit for demo interface

## Setup
```bash
pip install -r requirements.txt
```

## Data Acquisition

### Download Product and Review Data
```bash
python scripts/download_data.py
```

This will download:
- 50K Amazon Electronics products
- 100K customer reviews

### Generate Store Policies
```bash
python scripts/generate_policies.py
```

This creates realistic e-commerce policies:
- Return policy
- Shipping policy  
- Warranty information
- Payment methods
- FAQs


## Data Processing

After downloading raw data, process it into RAG-ready format:
```bash
python scripts/process_data.py
```

This will:
- Parse product metadata and reviews
- Chunk long documents
- Create unified document format
- Save to `data/processed/documents.json`

## Environment Setup

Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Required API keys:
- OpenAI API key for embeddings and LLM


## Building the Vector Store

After processing data, build the vector store:
```bash
python scripts/build_vector_store.py
```

This will:
- Load processed documents
- Generate embeddings using OpenAI
- Index documents in ChromaDB
- Create persistent vector store

**Note**: This step requires OpenAI API key and may take 10-15 minutes depending on dataset size.

## Usage

### Python API
```python
from src.rag_pipeline import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline()

# Ask a question
result = pipeline.query("What's the best laptop for students?")

print(result['answer'])
print(f"Based on {result['num_sources']} sources")
```

### Test Queries
```bash
python src/rag_pipeline.py
```


## API Usage

### Start the API Server
```bash
python src/api.py
```

API will be available at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example API Request
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the best laptop for students?",
    "return_sources": true
  }'
```

### Test the API
```bash
python scripts/test_api.py
```


## Demo Interface

### Launch Streamlit App
```bash
streamlit run app.py
```

Or use the script:
```bash
bash scripts/start_app.sh
```

The app will open in your browser at `http://localhost:8501`

### Features
- 🔍 Interactive search interface
- 📊 Real-time statistics
- 📚 Source document display
- 🎯 Filter by document type
- 💡 Example queries


## Testing & Evaluation

### Run Evaluation Suite

Test the RAG system with predefined queries:
```bash
python tests/test_queries.py
```

This will:
- Test 15+ sample queries across different categories
- Measure response latency
- Check retrieval quality
- Generate evaluation report

### Evaluation Metrics

- **Latency**: Response time per query
- **Retrieval Quality**: Relevant document types in top results
- **Success Rate**: Percentage of queries with expected doc types
- **Coverage**: Categories tested (product search, reviews, policies)

### Sample Queries

See `tests/sample_queries.md` for 50+ test queries organized by:
- Product search (budget, features, use case)
- Review analysis (sentiment, features, reliability)
- Policy questions (returns, shipping, warranty)
- Comparisons
- Complex/edge cases


## Coming Soon
- RAG implementation
- Demo interface