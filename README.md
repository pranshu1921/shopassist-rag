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


## Coming Soon
- RAG implementation
- Demo interface