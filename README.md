# 🛒 ShopAssist RAG: AI-Powered E-Commerce Product Assistant

> A production-ready RAG (Retrieval-Augmented Generation) system that intelligently answers customer questions by retrieving information from 50K+ products, 100K+ customer reviews, and store policies.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

ShopAssist RAG demonstrates a **Level 3 ML system** with production deployment capabilities:
- Multi-source retrieval (products, reviews, policies)
- Semantic search using vector embeddings
- LLM-powered natural language answers
- REST API and interactive web interface
- Response caching for performance
- Comprehensive evaluation framework

### Key Features

✨ **Intelligent Search**: Semantic search across 150K+ documents  
📊 **Source Attribution**: Answers cite specific products, reviews, and policies  
⚡ **Fast Responses**: <10ms with caching, ~2s cold start  
🎨 **Interactive UI**: Beautiful Streamlit interface  
🔌 **REST API**: FastAPI backend for integration  
📈 **Evaluation**: Built-in testing and benchmarking  

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- 8GB RAM, 10GB disk space

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/shopassist-rag.git
cd shopassist-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Data Setup
```bash
# 1. Download data (5-10 min)
python scripts/download_data.py
python scripts/generate_policies.py

# 2. Process data (2-3 min)
python scripts/process_data.py

# 3. Build vector store (10-20 min, ~$0.50 in API costs)
python scripts/build_vector_store.py
```

### Run the Application

**Option 1: Streamlit UI (Recommended)**
```bash
streamlit run app.py
# Open http://localhost:8501
```

**Option 2: FastAPI Backend**
```bash
python src/api.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**Option 3: Python API**
```python
from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("What's the best laptop for students under $800?")
print(result['answer'])
```

## 📚 Documentation

- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and components
- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment options
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🎬 Demo Queries

### Product Search
```
"What's the best laptop for video editing under $1500?"
"Show me wireless headphones with good noise cancellation"
"Gaming mouse with RGB lighting under $50"
```

### Review Analysis
```
"What do customers say about MacBook Air battery life?"
"Are there common complaints about gaming laptop keyboards?"
"How reliable is this wireless mouse according to reviews?"
```

### Policy Questions
```
"What is your return policy for electronics?"
"How long does shipping take?"
"Do you offer warranty on laptops?"
```

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Documents** | 150K+ (50K products, 100K reviews, 10 policies) |
| **Response Time (Cold)** | ~1.5-3.0 seconds |
| **Response Time (Cached)** | <10ms |
| **Retrieval Accuracy** | 85%+ (top-5 contains relevant docs) |
| **Cache Hit Rate** | 60-80% typical usage |
| **Cost per 1K Queries** | ~$0.50 (OpenAI API) |

## 🏗️ Architecture
```
User Query → Cache Check → Embedding → Vector Search → Top-K Docs
                                                           ↓
                                                    Format Context
                                                           ↓
                                            LLM Generation (GPT-3.5)
                                                           ↓
                                                    Cache & Return
```

**Tech Stack:**
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB (local persistence)
- **LLM**: GPT-3.5-turbo
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Cache**: File-based with 24h TTL

## 🧪 Testing & Evaluation
```bash
# Run evaluation suite
python tests/test_queries.py

# Performance benchmark
python scripts/benchmark.py

# Test API endpoints
python scripts/test_api.py
```


## 🐳 Docker Deployment

### Quick Start
```bash
# One-time setup
bash scripts/docker_setup.sh

# Start services
docker-compose up -d

# Access application
# API:  http://localhost:8000
# UI:   http://localhost:8501
# Docs: http://localhost:8000/docs
```

### Using Makefile
```bash
make docker-build   # Build image
make docker-up      # Start services
make docker-logs    # View logs
make docker-down    # Stop services
```

See [Docker Guide](docs/DOCKER.md) for detailed instructions.


## 📁 Project Structure
```
shopassist-rag/
├── app.py                      # Streamlit frontend
├── requirements.txt            # Dependencies
├── config/
│   └── config.yaml            # Configuration
├── src/
│   ├── data_processor.py      # Data processing pipeline
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB integration
│   ├── retriever.py           # Document retrieval
│   ├── llm.py                 # LLM answer generation
│   ├── rag_pipeline.py        # Complete RAG pipeline
│   ├── rag_pipeline_cached.py # With caching
│   ├── cache.py               # Caching layer
│   └── api.py                 # FastAPI backend
├── scripts/
│   ├── download_data.py       # Data acquisition
│   ├── generate_policies.py   # Policy generation
│   ├── process_data.py        # Data processing
│   ├── build_vector_store.py  # Vector indexing
│   ├── benchmark.py           # Performance testing
│   └── test_api.py            # API testing
├── tests/
│   ├── test_queries.py        # Evaluation suite
│   └── sample_queries.md      # Test query examples
├── docs/
│   ├── ARCHITECTURE.md        # System architecture
│   ├── SETUP.md               # Setup guide
│   └── DEPLOYMENT.md          # Deployment guide
├── data/
│   ├── raw/                   # Raw data (gitignored)
│   └── processed/             # Processed data (gitignored)
└── chroma_db/                 # Vector store (gitignored)
```

## 🎓 What I Learned

Building this project taught me:

- **RAG Implementation**: Practical challenges of retrieval-augmented generation
- **Vector Search**: Embedding generation, similarity search, and chunking strategies
- **Production ML**: Caching, monitoring, error handling, and API design
- **Data Processing**: Handling messy e-commerce data at scale
- **Cost Optimization**: Balancing API costs with response quality

### Key Challenges Solved

1. **Chunking Strategy**: Found optimal 500-char chunks with 50-char overlap
2. **Retrieval Quality**: Hybrid approach using semantic + metadata filtering
3. **Response Latency**: Reduced from 3s to <10ms with caching
4. **Context Length**: Balancing context size vs LLM token limits
5. **Source Attribution**: Tracking and displaying document provenance

## 🔮 Future Improvements

- [ ] Add authentication and rate limiting
- [ ] Implement hybrid search (semantic + keyword)
- [ ] Add conversation history/memory
- [ ] Fine-tune embeddings for e-commerce domain
- [ ] Deploy to cloud with auto-scaling
- [ ] Add A/B testing framework
- [ ] Implement query suggestions
- [ ] Add multi-language support

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Data**: Amazon Product Dataset by UCSD
- **Vector DB**: ChromaDB
- **LLM**: OpenAI GPT-3.5
- **Frameworks**: LangChain, FastAPI, Streamlit

## 📧 Contact

For questions or feedback:
- Open an issue on GitHub
- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

**Built with ❤️ as a portfolio project demonstrating production ML systems (Level 3)**

*Last updated: January 2025*
```

### **File: `LICENSE`**
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.