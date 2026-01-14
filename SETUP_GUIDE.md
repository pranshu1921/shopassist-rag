# ShopAssist RAG - Complete Setup & Run Guide

This guide provides **exact, step-by-step instructions** to get the ShopAssist RAG system running on your local machine.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.9 or higher** installed
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- [ ] **pip** (Python package manager) installed
  - Check: `pip --version` or `pip3 --version`
  - Usually comes with Python

- [ ] **Git** installed
  - Check: `git --version`
  - Download: https://git-scm.com/downloads

- [ ] **OpenAI API Key**
  - Sign up: https://platform.openai.com/signup
  - Get API key: https://platform.openai.com/api-keys
  - Need credit card on file (will cost ~$0.50 to build vector store)

- [ ] **8GB+ RAM** (16GB recommended)

- [ ] **10GB+ free disk space**

- [ ] **Internet connection** (for downloading data)

---

## 🔧 Step 1: Clone the Repository

### Option A: Clone from GitHub (Recommended)

```bash
# Navigate to where you want the project
cd ~/projects  # or any directory you prefer

# Clone the repository
git clone https://github.com/yourusername/shopassist-rag.git

# Navigate into the project
cd shopassist-rag
```

### Option B: Create from Scratch

```bash
# Create project directory
mkdir shopassist-rag
cd shopassist-rag

# Initialize git
git init

# Create all the files we discussed in commits 1-12
# (You'll need to manually create each file)
```

---

## 🐍 Step 2: Set Up Python Virtual Environment

### On macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your terminal prompt should now show (venv)
```

### On Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Your terminal prompt should now show (venv)
```

### Verification:

```bash
# Check that you're using the virtual environment's Python
which python  # macOS/Linux
where python  # Windows

# Should show path to venv/bin/python or venv\Scripts\python
```

---

## 📦 Step 3: Install Dependencies

```bash
# Make sure virtual environment is activated (you should see (venv) in terminal)

# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# This will take 2-5 minutes depending on your internet speed
```

### Expected Packages:
- langchain
- langchain-openai
- chromadb
- openai
- fastapi
- uvicorn
- streamlit
- python-dotenv
- pandas
- tqdm
- pyyaml
- requests

### Verify Installation:

```bash
# Check that key packages are installed
pip list | grep langchain
pip list | grep chromadb
pip list | grep openai
pip list | grep streamlit
```

---

## 🔑 Step 4: Configure Environment Variables

### Create .env File:

```bash
# Copy the example file
cp .env.example .env

# On Windows:
# copy .env.example .env
```

### Edit .env File:

Open `.env` in your text editor:

```bash
# Using nano (Linux/Mac)
nano .env

# Using vim
vim .env

# Using VS Code
code .env

# On Windows, use Notepad
notepad .env
```

Add your OpenAI API key:

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional: API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

**IMPORTANT:** Replace `sk-proj-xxxxx...` with your actual OpenAI API key!

### Verify .env File:

```bash
# Check that file exists
ls -la .env  # macOS/Linux
dir .env     # Windows

# Check contents (be careful not to share this!)
cat .env     # macOS/Linux
type .env    # Windows
```

---

## 📊 Step 5: Download Data

This step downloads Amazon product and review data (~200MB total).

```bash
# Download Amazon Electronics data
python scripts/download_data.py
```

**What this does:**
- Downloads `meta_Electronics.json.gz` (161 MB)
- Downloads `Electronics.json.gz` (6.89 GB compressed)
- Extracts and samples 50K products
- Extracts and samples 100K reviews
- Saves to `data/raw/`

**Expected time:** 5-10 minutes (depends on internet speed)

**Expected output:**
```
Downloading Amazon product metadata...
[████████████████████████████████] 161 MB / 161 MB
Extracting product data...
Sampling 50,000 products...
✓ Saved to data/raw/products_50k.json

Downloading Amazon reviews...
[████████████████████████████████] 6.89 GB / 6.89 GB
Extracting review data...
Sampling 100,000 reviews...
✓ Saved to data/raw/reviews_100k.json
```

### Generate Store Policies:

```bash
# Generate synthetic policy documents
python scripts/generate_policies.py
```

**Expected time:** <1 minute

**Expected output:**
```
Generating store policy documents...
✓ Created data/raw/return_policy.md
✓ Created data/raw/shipping_policy.md
✓ Created data/raw/warranty_info.md
✓ Created data/raw/payment_methods.md
✓ Created data/raw/faq.md
```

### Verify Data Files:

```bash
# Check that files were created
ls -lh data/raw/

# Should see:
# products_50k.json (~60 MB)
# reviews_100k.json (~150 MB)
# return_policy.md
# shipping_policy.md
# warranty_info.md
# payment_methods.md
# faq.md
```

---

## 🔄 Step 6: Process Data

This step converts raw data into RAG-ready documents.

```bash
python scripts/process_data.py
```

**What this does:**
- Loads products, reviews, and policies
- Chunks long documents (500 chars with 50 char overlap)
- Creates unified document format
- Saves to `data/processed/documents.json`

**Expected time:** 2-3 minutes

**Expected output:**
```
==============================
Processing Data for RAG
==============================

Loading products...
✓ Loaded 50,000 products

Loading reviews...
✓ Loaded 100,000 reviews

Loading policies...
✓ Loaded 5 policy documents

Processing products...
Processing: 100%|████████████████| 50000/50000

Processing reviews...
Processing: 100%|████████████████| 100000/100000

Processing policies...
Processing: 100%|████████████████| 5/5

==============================
✓ Processing complete!
==============================
Total documents created: 152,341
Saved to: data/processed/documents.json
```

### Verify Processed Data:

```bash
# Check file was created
ls -lh data/processed/

# Should see:
# documents.json (~100 MB)
```

---

## 🗂️ Step 7: Build Vector Store

**⚠️ IMPORTANT:** This step uses OpenAI API and will cost approximately **$0.50**

```bash
python scripts/build_vector_store.py
```

**What this does:**
- Loads processed documents
- Generates embeddings using OpenAI (text-embedding-3-small)
- Indexes documents in ChromaDB
- Creates persistent vector store in `chroma_db/`

**Expected time:** 10-20 minutes (depends on API speed)

**Expected output:**
```
============================================================
Building Vector Store
============================================================

Loading processed documents...
✓ Loaded 152,341 documents

Initializing vector store...
✓ ChromaDB initialized

Adding documents to vector store...
Indexing: 100%|████████████████| 1524/1524 batches
✓ Added 152,341 documents to vector store

============================================================
✓ Vector store built successfully!
============================================================
Total documents indexed: 152,341

Testing search...
Query: 'laptop for gaming'
Found 3 results:
1. [product] Score: 0.892
   ASUS ROG Strix Gaming Laptop...
```

### Verify Vector Store:

```bash
# Check that ChromaDB directory was created
ls -la chroma_db/

# Should see:
# chroma.sqlite3
# (and other ChromaDB files)
```

---

## 🎯 Step 8: Run the Application

You can now run the application in three different ways:

### **Option A: Streamlit Web Interface (RECOMMENDED for Demo)**

```bash
# Make sure you're in the project root and venv is activated
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

**Access the app:**
- Open your browser
- Go to: http://localhost:8501
- You should see the ShopAssist RAG interface

**Using the UI:**
1. Type a question in the text box (e.g., "What's the best laptop for students?")
2. Click "Search" button
3. View the AI-generated answer
4. See source documents below the answer

**To stop:**
- Press `Ctrl+C` in the terminal

---

### **Option B: FastAPI REST API**

```bash
# Make sure you're in the project root and venv is activated
python src/api.py
```

**Expected output:**
```
Starting ShopAssist RAG API on 0.0.0.0:8000
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Access the API:**
- API endpoint: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

**Test the API:**

In another terminal:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test query endpoint
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the best laptop for students?",
    "return_sources": true
  }'
```

**To stop:**
- Press `Ctrl+C` in the terminal

---

### **Option C: Python API (Programmatic)**

Create a test script:

```bash
# Create test file
nano test_rag.py  # or use your editor
```

Add this code:

```python
from src.rag_pipeline import RAGPipeline

# Initialize pipeline
print("Initializing RAG pipeline...")
pipeline = RAGPipeline()

# Test query
query = "What's the best laptop for students under $800?"
print(f"\nQuery: {query}")

# Get answer
result = pipeline.query(query)

# Display results
print(f"\nAnswer: {result['answer']}")
print(f"\nBased on {result['num_sources']} sources:")
for i, source in enumerate(result['sources'], 1):
    print(f"{i}. {source['type']} (score: {source['score']:.2f})")
```

Run it:

```bash
python test_rag.py
```

**Expected output:**
```
Initializing RAG pipeline...
Query: What's the best laptop for students under $800?

Answer: Based on customer reviews and product specifications, the Dell 
Inspiron 15 3000 and Acer Aspire 5 are excellent options for students...

Based on 5 sources:
1. product (score: 0.89)
2. product (score: 0.85)
3. review (score: 0.82)
4. product (score: 0.79)
5. review (score: 0.76)
```

---

## ✅ Step 9: Verify Everything Works

### Run Tests:

```bash
# Run evaluation suite
python tests/test_queries.py
```

**Expected output:**
```
======================================================================
ShopAssist RAG - Evaluation
======================================================================

📊 Category: product_search
----------------------------------------------------------------------
✓ Query: Show me laptops under $1000 with at least 16GB RAM
   Latency: 1847ms
   Sources: 5 (product, product, product, review, review)
   Answer: Based on our catalog, here are some excellent laptops...
...

📈 Overall Statistics
======================================================================
Total Queries: 15
Average Latency: 1624.32ms
Overall Success Rate: 86.67%
```

### Benchmark Performance:

```bash
# Run performance benchmark
python scripts/benchmark.py
```

**Expected output:**
```
======================================================================
ShopAssist RAG - Performance Benchmark
======================================================================

Benchmarking 5 queries (3 runs each)...

--- Run 1/3 ---
1. [MISS] 1823.4ms - What's the best laptop for students under $800?...
2. [MISS] 1654.2ms - Show me wireless headphones with noise cancella...
3. [MISS] 1432.8ms - What is your return policy?...
4. [MISS] 1876.5ms - What do customers say about gaming laptops?...
5. [MISS] 1598.3ms - Which smartphone has the best camera?...

--- Run 2/3 ---
1. [HIT]    8.2ms - What's the best laptop for students under $800?...
2. [HIT]    6.7ms - Show me wireless headphones with noise cancella...
3. [HIT]    5.9ms - What is your return policy?...
4. [HIT]    7.3ms - What do customers say about gaming laptops?...
5. [HIT]    6.1ms - Which smartphone has the best camera?...

======================================================================
Performance Summary
======================================================================
Query Statistics:
  Total Queries: 15
  Cache Hits: 10
  Cache Misses: 5
  Cache Hit Rate: 66.7%

Latency:
  Average: 567.4ms
  Total: 8511.2ms

Cache:
  Entries: 5
  Size: 0.03 MB
```

---

## 🐳 Optional: Docker Deployment

If you want to run with Docker:

### Prerequisites:
- Docker installed
- Docker Compose installed

### Setup:

```bash
# Run Docker setup script
bash scripts/docker_setup.sh

# Or manually:
docker-compose build
docker-compose up -d
```

### Access:
- API: http://localhost:8000
- UI: http://localhost:8501
- Docs: http://localhost:8000/docs

### Stop:
```bash
docker-compose down
```

---

## 🎓 Quick Start Summary

For future reference, once everything is set up:

```bash
# 1. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. Run Streamlit UI
streamlit run app.py

# OR run FastAPI
python src/api.py

# OR use Python API
python test_rag.py
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check contents
cat .env  # Should show OPENAI_API_KEY=sk-...

# If missing, create it:
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Issue: "Module not found"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "ChromaDB collection not found"

**Solution:**
```bash
# Rebuild vector store
python scripts/build_vector_store.py
```

### Issue: "Out of memory"

**Solution:**
- Reduce data limits in `config/config.yaml`:
  - `products_limit: 10000` (instead of 50000)
  - `reviews_limit: 20000` (instead of 100000)
- Rerun: `python scripts/process_data.py`
- Rerun: `python scripts/build_vector_store.py`

### Issue: "Slow responses"

**Solution:**
- First query is always slow (cold start) - this is normal
- Subsequent queries should be <10ms (cached)
- Check cache is enabled in `config/config.yaml`

### Issue: "Port already in use"

**Solution:**
```bash
# For Streamlit (port 8501)
lsof -ti:8501 | xargs kill  # macOS/Linux
netstat -ano | findstr :8501  # Windows - note PID
taskkill /PID [PID] /F  # Windows - kill process

# For FastAPI (port 8000)
lsof -ti:8000 | xargs kill  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

## 📞 Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review `docs/SETUP.md` for detailed instructions
3. Check `docs/ARCHITECTURE.md` for system overview
4. Open an issue on GitHub
5. Check OpenAI API status: https://status.openai.com/

---

## ✅ Success Checklist

You've successfully set up ShopAssist RAG if:

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file created with OpenAI API key
- [ ] Data downloaded (3 files in `data/raw/`)
- [ ] Data processed (`documents.json` in `data/processed/`)
- [ ] Vector store built (`chroma_db/` directory exists)
- [ ] Streamlit app launches without errors
- [ ] Test query returns a relevant answer
- [ ] Evaluation tests pass

---

## 🎉 You're Ready!

Your ShopAssist RAG system is now fully operational. Try asking questions like:

- "What's the best laptop for video editing under $1500?"
- "Show me wireless headphones with good reviews"
- "What do customers say about MacBook Air battery life?"
- "What is your return policy?"

**Enjoy your production-ready RAG system!** 🚀
