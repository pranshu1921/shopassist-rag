# ShopAssist RAG - Architecture Overview

## System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌──────────────────┐              ┌───────────────────┐   │
│  │  Streamlit App   │              │   FastAPI REST    │   │
│  │   (app.py)       │              │   (src/api.py)    │   │
│  └──────────────────┘              └───────────────────┘   │
└──────────────┬─────────────────────────────┬────────────────┘
               │                             │
               └──────────────┬──────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   RAG Pipeline    │
                    │ (Cached Version)  │
                    │  src/rag_*.py     │
                    └─────────┬─────────┘
                              │
          ┏───────────────────┼───────────────────┓
          │                   │                   │
    ┌─────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
    │  Retriever │    │     LLM     │    │    Cache    │
    │  (Vector   │    │  Generator  │    │   (File-    │
    │   Search)  │    │  (OpenAI)   │    │    based)   │
    └─────┬──────┘    └─────────────┘    └─────────────┘
          │
    ┌─────▼──────┐
    │  ChromaDB  │
    │   Vector   │
    │   Store    │
    └─────┬──────┘
          │
    ┌─────▼──────┐
    │  Embedding │
    │  Generator │
    │  (OpenAI)  │
    └────────────┘
```

## Component Details

### 1. Data Layer

#### Data Sources
- **Products**: 50K Amazon Electronics products
- **Reviews**: 100K customer reviews
- **Policies**: 5 store policy documents

#### Data Processing (`src/data_processor.py`)
- Parses JSON product and review data
- Loads markdown policy documents
- Chunks long documents (500 chars with 50 char overlap)
- Creates unified document format with metadata

### 2. Storage Layer

#### Vector Database (`src/vector_store.py`)
- **Technology**: ChromaDB
- **Embedding Model**: OpenAI text-embedding-3-small (1536 dimensions)
- **Distance Metric**: Cosine similarity
- **Persistence**: Local disk storage in `./chroma_db`

#### Cache (`src/cache.py`)
- **Type**: File-based cache
- **TTL**: 24 hours (configurable)
- **Location**: `.cache/` directory
- **Format**: JSON files named by query hash

### 3. Retrieval Layer

#### Retriever (`src/retriever.py`, `src/vector_store.py`)
- Semantic search using vector similarity
- Top-K retrieval (default: 5 documents)
- Optional filtering by document type
- Simple keyword-based re-ranking

### 4. Generation Layer

#### LLM Generator (`src/llm.py`)
- **Model**: GPT-3.5-turbo
- **Temperature**: 0.1 (factual responses)
- **Max Tokens**: 500
- **Prompt Engineering**: System prompt for e-commerce assistant role

### 5. Application Layer

#### RAG Pipeline (`src/rag_pipeline.py`, `src/rag_pipeline_cached.py`)
- Orchestrates retrieval + generation
- Handles source attribution
- Implements caching layer
- Tracks performance metrics

#### REST API (`src/api.py`)
- FastAPI framework
- Endpoints: `/query`, `/health`, `/stats`, `/examples`
- CORS enabled for web access
- Pydantic models for validation

#### Web Interface (`app.py`)
- Streamlit-based UI
- Interactive query input
- Source document display
- Real-time statistics

## Data Flow

### Query Processing Flow
```
User Query
    ↓
Cache Check
    ↓ (miss)
Generate Embedding (OpenAI)
    ↓
Vector Search (ChromaDB)
    ↓
Retrieve Top-K Documents
    ↓
Format Context
    ↓
LLM Generation (OpenAI)
    ↓
Cache Result
    ↓
Return Answer + Sources
```

### Performance Characteristics

| Operation | Latency (Cold) | Latency (Cached) |
|-----------|---------------|------------------|
| Embedding Generation | ~100ms | N/A |
| Vector Search | ~50ms | N/A |
| LLM Generation | ~1000-2000ms | N/A |
| **Total (Cache Miss)** | **~1500-3000ms** | **<10ms** |

## Configuration

All configuration is centralized in `config/config.yaml`:

- Data processing parameters
- Embedding model settings
- LLM parameters
- Vector DB configuration
- API settings
- Cache settings

## Scalability Considerations

### Current Limitations (Level 3)
- Single-node deployment
- File-based caching (not distributed)
- Synchronous processing
- Local vector store

### Future Enhancements (Level 4)
- Distributed vector store (Pinecone, Weaviate cloud)
- Redis caching for distributed systems
- Async processing with queues
- Horizontal scaling with load balancer
- GPU-accelerated inference

## Security Considerations

- API keys stored in `.env` (not committed)
- No authentication (demo purposes)
- CORS enabled (configure for production)
- Input validation via Pydantic models
- Rate limiting not implemented (add for production)

## Monitoring & Observability

### Metrics Tracked
- Query latency
- Cache hit rate
- Total queries processed
- Document retrieval statistics
- Vector store size

### Logs
- Query logs (user questions)
- Error logs (failures, exceptions)
- Performance logs (latency tracking)

## Cost Analysis

### OpenAI API Costs (Estimated)

**For 1000 Queries:**
- Embeddings (1000 queries): ~$0.013
- LLM Generation (1000 queries): ~$0.50
- **Total**: ~$0.51 per 1000 queries

**Monthly (10K queries):**
- ~$5/month

### Infrastructure Costs
- ChromaDB: Free (local)
- Storage: <1GB (negligible)
- Compute: Local machine (free) or cloud VM (~$10-30/month)

**Total Estimated Monthly Cost: $5-35**