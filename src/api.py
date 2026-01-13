"""
FastAPI backend for ShopAssist RAG
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import yaml

from src.rag_pipeline import RAGPipeline

# Initialize FastAPI app
app = FastAPI(
    title="ShopAssist RAG API",
    description="AI-Powered E-Commerce Product Assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open("config/config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Initialize RAG pipeline (lazy loading)
rag_pipeline = None


def get_pipeline():
    """Lazy load RAG pipeline"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline


# Request/Response models
class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., description="Customer question", min_length=3)
    return_sources: bool = Field(True, description="Include source documents")
    filter_type: Optional[str] = Field(None, description="Filter by type: product, review, or policy")


class SourceDocument(BaseModel):
    """Source document model"""
    type: str
    score: float
    content_preview: str
    metadata: Dict[str, Any]


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    query: str
    sources: Optional[List[SourceDocument]] = None
    num_sources: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    total_documents: int


# API endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "ShopAssist RAG API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        pipeline = get_pipeline()
        stats = pipeline.get_stats()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            total_documents=stats['total_documents']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system
    
    Example request:
```json
    {
        "query": "What's the best laptop for students?",
        "return_sources": true
    }
```
    """
    try:
        pipeline = get_pipeline()
        
        result = pipeline.query(
            query=request.query,
            return_sources=request.return_sources,
            filter_type=request.filter_type
        )
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get pipeline statistics"""
    try:
        pipeline = get_pipeline()
        return pipeline.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


# Example queries endpoint
@app.get("/examples")
async def get_example_queries():
    """Get example queries to try"""
    return {
        "product_queries": [
            "What's the best laptop for gaming under $1500?",
            "Show me affordable wireless headphones with good reviews",
            "Which smartphone has the best camera for under $700?"
        ],
        "review_queries": [
            "What do customers say about MacBook Air battery life?",
            "Are there any complaints about this laptop's keyboard?",
            "How reliable is this brand according to reviews?"
        ],
        "policy_queries": [
            "What is your return policy for electronics?",
            "How long does shipping take?",
            "Do you offer warranty on laptops?"
        ]
    }


if __name__ == "__main__":
    # Get API config
    host = config['api']['host']
    port = config['api']['port']
    
    print(f"Starting ShopAssist RAG API on {host}:{port}")
    print(f"Docs available at http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)