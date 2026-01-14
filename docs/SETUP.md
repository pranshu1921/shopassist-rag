# ShopAssist RAG - Complete Setup Guide

## Prerequisites

### System Requirements
- Python 3.9 or higher
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space
- Internet connection for downloading data

### Required Accounts
- OpenAI API account with API key

## Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/shopassist-rag.git
cd shopassist-rag
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

Add to `.env`:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Download Data
```bash
# Download Amazon product and review data
python scripts/download_data.py

# Generate store policies
python scripts/generate_policies.py
```

**Expected output:**
- `data/raw/products_50k.json` (~60MB)
- `data/raw/reviews_100k.json` (~150MB)
- `data/raw/*.md` (policy files)

**Time required:** 5-10 minutes depending on internet speed

### 6. Process Data
```bash
python scripts/process_data.py
```

**Expected output:**
- `data/processed/documents.json` (~100MB)

**Time required:** 2-3 minutes

### 7. Build Vector Store
```bash
python scripts/build_vector_store.py
```

This step:
- Generates embeddings for all documents
- Indexes documents in ChromaDB
- Creates persistent vector store

**Expected output:**
- `chroma_db/` directory with indexed data

**Time required:** 10-20 minutes
**Cost:** ~$0.50 in OpenAI API calls

### 8. Verify Setup
```bash
# Test the RAG pipeline
python src/rag_pipeline.py
```

You should see test queries being processed successfully.

## Running the Application

### Option 1: Streamlit UI (Recommended for Demo)
```bash
streamlit run app.py
```

Access at: http://localhost:8501

### Option 2: FastAPI Backend
```bash
python src/api.py
```

Access at: http://localhost:8000
API docs: http://localhost:8000/docs

### Option 3: Python API
```python
from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("What's the best laptop for students?")
print(result['answer'])
```

## Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
- Make sure `.env` file exists in project root
- Check that `OPENAI_API_KEY` is set correctly
- Restart your terminal/IDE after setting environment variable

### Issue: "ChromaDB collection not found"

**Solution:**
- Run `python scripts/build_vector_store.py` to create the index
- Check that `chroma_db/` directory exists
- Make sure you didn't skip the data processing step

### Issue: "Memory error during vector store build"

**Solution:**
- Reduce `products_limit` and `reviews_limit` in `config/config.yaml`
- Process in smaller batches
- Use a machine with more RAM

### Issue: "Slow query responses"

**Solution:**
- First query is always slow (cold start)
- Enable caching: use `CachedRAGPipeline` instead of `RAGPipeline`
- Reduce `top_k` in config (fewer documents retrieved)
- Use smaller embedding model (change in config)

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Data download fails"

**Solution:**
- Check internet connection
- Download files manually from URLs in `scripts/download_data.py`
- Place files in `data/raw/` directory

## Validation Checklist

After setup, verify:

- [ ] `.env` file exists with OpenAI API key
- [ ] `data/raw/` contains 3+ files (products, reviews, policies)
- [ ] `data/processed/documents.json` exists and is ~100MB
- [ ] `chroma_db/` directory exists
- [ ] `python src/rag_pipeline.py` runs without errors
- [ ] Streamlit app launches successfully
- [ ] Test query returns a relevant answer

## Next Steps

1. Run evaluation: `python tests/test_queries.py`
2. Benchmark performance: `python scripts/benchmark.py`
3. Try example queries in Streamlit UI
4. Customize configuration in `config/config.yaml`
5. Deploy (see `docs/DEPLOYMENT.md`)

## Getting Help

- Check `docs/ARCHITECTURE.md` for system overview
- Review `tests/sample_queries.md` for query examples
- See `README.md` for quick reference
- Open an issue on GitHub for bugs