# 🛒 ShopAssist RAG: AI-Powered E-Commerce Product Assistant

> A production-ready RAG (Retrieval-Augmented Generation) system that intelligently answers customer questions by retrieving information from 50K+ products, 100K+ customer reviews, and store policies.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

ShopAssist RAG is an intelligent shopping assistant that combines semantic search with large language models to answer customer questions naturally. The system retrieves relevant information from multiple data sources and generates accurate, contextual responses with source attribution.

### Key Features

✨ **Intelligent Search**: Semantic search across 150K+ documents using vector embeddings  
📊 **Source Attribution**: Answers cite specific products, reviews, and store policies  
⚡ **Fast Responses**: Sub-10ms latency with intelligent caching, ~2s for complex queries  
🎨 **Interactive UI**: Beautiful Streamlit interface for easy interaction  
🔌 **REST API**: FastAPI backend for seamless integration  
📈 **Evaluation Suite**: Built-in testing and performance benchmarking  
🐳 **Docker Ready**: Containerized deployment for production environments  

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

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

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Data Setup
```bash
# 1. Download data (5-10 minutes)
python scripts/download_data.py
python scripts/generate_policies.py

# 2. Process data (2-3 minutes)
python scripts/process_data.py

# 3. Build vector store (10-20 minutes, ~$0.50 in API costs)
python scripts/build_vector_store.py
```

### Run the Application

**Option 1: Streamlit UI (Recommended for Demo)**
```bash
streamlit run app.py
# Open http://localhost:8501 in your browser
```

**Option 2: FastAPI Backend**
```bash
python src/api.py
# API: http://localhost:8000
# Interactive API docs: http://localhost:8000/docs
```

**Option 3: Python API**
```python
from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("What's the best laptop for students under $800?")
print(result['answer'])
print(f"Sources: {result['num_sources']}")
```

## 🐳 Docker Deployment

### Quick Start with Docker
```bash
# One-time setup
bash scripts/docker_setup.sh

# Start services
docker-compose up -d

# Access application
# API:  http://localhost:8000
# UI:   http://localhost:8501
# Docs: http://localhost:8000/docs

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Makefile
```bash
make docker-build   # Build Docker image
make docker-up      # Start services
make docker-logs    # View logs
make docker-down    # Stop services
```

See [Docker Guide](docs/DOCKER.md) for detailed deployment instructions.

## 📚 Documentation

- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and technical details
- **[Setup Guide](docs/SETUP.md)** - Step-by-step installation and configuration
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment options
- **[Docker Guide](docs/DOCKER.md)** - Container deployment instructions
- **[Contributing](CONTRIBUTING.md)** - Guidelines for contributing to the project

## 🎬 Demo Queries

### Product Search
```
"What's the best laptop for video editing under $1500?"
"Show me wireless headphones with good noise cancellation"
"Gaming mouse with RGB lighting under $50"
"Smartphone with best camera for photography"
```

### Review Analysis
```
"What do customers say about MacBook Air battery life?"
"Are there common complaints about gaming laptop keyboards?"
"How reliable is this wireless mouse according to reviews?"
"Customer feedback on noise cancellation quality"
```

### Policy Questions
```
"What is your return policy for electronics?"
"How long does standard shipping take?"
"Do you offer warranty on laptops?"
"What payment methods do you accept?"
```

### Comparison Queries
```
"Compare MacBook Air vs Dell XPS 13 for students"
"iPhone 14 vs Samsung Galaxy S23 camera quality"
"Which has better battery: laptop A or laptop B?"
```

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Documents Indexed** | 150K+ (50K products, 100K reviews, 10 policies) |
| **Response Time (Cold Start)** | ~1.5-3.0 seconds |
| **Response Time (Cached)** | <10 milliseconds |
| **Retrieval Accuracy** | 85%+ relevant documents in top-5 results |
| **Cache Hit Rate** | 60-80% in typical usage patterns |
| **API Cost per 1K Queries** | ~$0.50 (OpenAI API) |
| **Storage Required** | ~1GB for vector store |

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    User Query                            │
└─────────────────────┬───────────────────────────────────┘
                      │
                ┌─────▼──────┐
                │ Cache Check │
                └─────┬──────┘
                      │ (miss)
            ┌─────────▼──────────┐
            │ Generate Embedding  │
            │    (OpenAI API)     │
            └─────────┬───────────┘
                      │
            ┌─────────▼───────────┐
            │   Vector Search     │
            │    (ChromaDB)       │
            └─────────┬───────────┘
                      │
            ┌─────────▼───────────┐
            │ Retrieve Top-K Docs │
            │  (5 most relevant)  │
            └─────────┬───────────┘
                      │
            ┌─────────▼───────────┐
            │  Format Context     │
            │ (Products, Reviews) │
            └─────────┬───────────┘
                      │
            ┌─────────▼───────────┐
            │  LLM Generation     │
            │   (GPT-3.5-turbo)   │
            └─────────┬───────────┘
                      │
            ┌─────────▼───────────┐
            │   Cache & Return    │
            │ (Answer + Sources)  │
            └─────────────────────┘
```

**Technology Stack:**
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **Vector Database**: ChromaDB with cosine similarity
- **LLM**: GPT-3.5-turbo with temperature 0.1
- **Backend Framework**: FastAPI with async support
- **Frontend**: Streamlit with interactive components
- **Caching**: File-based cache with 24-hour TTL
- **Deployment**: Docker and Docker Compose

## 🧪 Testing & Evaluation

### Run Evaluation Suite

Test the system with predefined queries across different categories:
```bash
python tests/test_queries.py
```

This evaluates:
- Product search accuracy
- Review analysis quality
- Policy question handling
- Response latency
- Source relevance

### Performance Benchmark
```bash
python scripts/benchmark.py
```

Measures:
- Average query latency
- Cache hit rate
- Query throughput
- API cost per query

### Test API Endpoints
```bash
# Start API first
python src/api.py

# In another terminal
python scripts/test_api.py
```

## 📁 Project Structure
```
shopassist-rag/
├── app.py                      # Streamlit web interface
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Multi-container setup
├── Makefile                    # Build automation
├── config/
│   └── config.yaml            # Centralized configuration
├── src/
│   ├── data_processor.py      # Data loading and processing
│   ├── embeddings.py          # OpenAI embedding generation
│   ├── vector_store.py        # ChromaDB integration
│   ├── retriever.py           # Document retrieval logic
│   ├── llm.py                 # LLM answer generation
│   ├── rag_pipeline.py        # Complete RAG pipeline
│   ├── rag_pipeline_cached.py # Pipeline with caching
│   ├── cache.py               # Response caching layer
│   └── api.py                 # FastAPI REST API
├── scripts/
│   ├── download_data.py       # Data acquisition
│   ├── generate_policies.py   # Policy document generation
│   ├── process_data.py        # Data preprocessing
│   ├── build_vector_store.py  # Vector database indexing
│   ├── benchmark.py           # Performance testing
│   ├── docker_setup.sh        # Docker setup automation
│   └── test_api.py            # API testing
├── tests/
│   ├── test_queries.py        # Evaluation framework
│   └── sample_queries.md      # Test query examples
├── docs/
│   ├── ARCHITECTURE.md        # System architecture
│   ├── SETUP.md               # Setup instructions
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── DOCKER.md              # Docker deployment
├── data/
│   ├── raw/                   # Raw data files (gitignored)
│   └── processed/             # Processed documents (gitignored)
└── chroma_db/                 # Vector store (gitignored)
```

## 🎓 What I Learned

Building this production RAG system provided hands-on experience with:

### Technical Skills
- **Vector Search**: Implementing semantic search with embeddings and similarity metrics
- **RAG Architecture**: Combining retrieval and generation for accurate, grounded responses
- **API Design**: Building RESTful APIs with proper error handling and validation
- **Caching Strategies**: Optimizing performance with intelligent response caching
- **Data Processing**: Handling large-scale e-commerce data with proper chunking

### Key Challenges & Solutions

**Challenge 1: Optimal Chunking Strategy**
- Problem: How to split documents without losing context
- Solution: 500-character chunks with 50-character overlap based on experimentation

**Challenge 2: Response Latency**
- Problem: 3-second response time too slow for production
- Solution: Implemented file-based caching, reducing to <10ms for cached queries

**Challenge 3: Source Attribution**
- Problem: Users need to verify answer accuracy
- Solution: Track and display source documents with metadata and relevance scores

**Challenge 4: Context Length Management**
- Problem: Balancing context size with LLM token limits
- Solution: Top-K retrieval (K=5) with careful prompt engineering

**Challenge 5: Cost Optimization**
- Problem: OpenAI API costs can add up quickly
- Solution: Aggressive caching + batch embedding generation = 80% cost reduction

### Production Considerations

- **Error Handling**: Comprehensive try-catch blocks and graceful degradation
- **Monitoring**: Performance metrics tracking and logging
- **Documentation**: Extensive docs for setup, architecture, and deployment
- **Testing**: Evaluation framework with 15+ test queries
- **Deployment**: Docker containerization for consistent environments

## 🔮 Future Improvements

### High Priority
- [ ] Add authentication and API key management
- [ ] Implement rate limiting for API endpoints
- [ ] Add conversation history/memory for multi-turn queries
- [ ] Implement hybrid search (semantic + keyword)
- [ ] Add query suggestions based on user history

### Medium Priority
- [ ] Fine-tune embeddings on e-commerce domain
- [ ] Add A/B testing framework for model comparison
- [ ] Implement real-time product inventory updates
- [ ] Add multi-language support (Spanish, French, etc.)
- [ ] Create mobile-friendly interface

### Nice to Have
- [ ] Voice interface using speech-to-text
- [ ] Advanced analytics dashboard
- [ ] Product recommendation engine
- [ ] Image-based product search
- [ ] Integration with actual e-commerce platforms

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development setup
- Testing requirements
- Pull request process

Areas where contributions would be valuable:
- Performance optimizations
- Additional data sources
- UI/UX improvements
- Documentation enhancements
- Test coverage expansion

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Dataset**: Amazon Product Data by UCSD (Jianmo Ni, Jiacheng Li, Julian McAuley)
- **Vector Database**: ChromaDB team for excellent documentation
- **LLM Provider**: OpenAI for GPT-3.5 and embedding models
- **Frameworks**: LangChain, FastAPI, and Streamlit communities

## 📧 Contact

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

## 📈 Project Stats

- **Development Time**: 6-8 weeks
- **Lines of Code**: ~3,000
- **Test Coverage**: 15+ evaluation queries
- **Documentation Pages**: 5 comprehensive guides
- **API Endpoints**: 5 (query, health, stats, examples, root)

---

**Built with ❤️ to demonstrate production machine learning systems and real-world AI applications**

*Star ⭐ this repository if you find it useful!*

*Last updated: January 2025*