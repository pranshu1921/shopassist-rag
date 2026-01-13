"""
LLM integration for answer generation
"""
import os
from typing import List, Optional
from openai import OpenAI
import yaml
from dotenv import load_dotenv

from src.retriever import RetrievedDocument

load_dotenv()


class LLMGenerator:
    """Generate answers using OpenAI LLM"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.model = self.config['llm']['model']
        self.temperature = self.config['llm']['temperature']
        self.max_tokens = self.config['llm']['max_tokens']
        
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_answer(
        self, 
        query: str, 
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate answer based on query and retrieved context"""
        
        if system_prompt is None:
            system_prompt = """You are a helpful e-commerce shopping assistant. Answer customer questions based on the provided product information, customer reviews, and store policies.

Guidelines:
- Be concise and helpful
- Cite specific products when relevant (mention product names)
- Reference customer reviews when discussing product experiences
- Mention prices when comparing products
- If the information isn't in the context, say so politely
- For policy questions, provide clear, accurate information
- Be friendly and professional"""
        
        user_prompt = f"""Context information from our store:
{context}

Customer Question: {query}

Please provide a helpful answer based on the context above."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content
    
    def generate_answer_with_sources(
        self,
        query: str,
        retrieved_docs: List[RetrievedDocument]
    ) -> dict:
        """Generate answer with source attribution"""
        
        # Format context from retrieved documents
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            doc_type_label = doc.doc_type.upper()
            context_parts.append(f"[SOURCE {i} - {doc_type_label}]")
            context_parts.append(doc.content)
            context_parts.append("")
            
            # Track sources
            source_info = {
                'id': i,
                'type': doc.doc_type,
                'score': doc.score,
                'metadata': doc.metadata
            }
            sources.append(source_info)
        
        context = "\n".join(context_parts)
        
        # Generate answer
        answer = self.generate_answer(query, context)
        
        return {
            'answer': answer,
            'sources': sources,
            'query': query
        }


if __name__ == "__main__":
    # Test LLM generation
    from src.vector_store import ChromaVectorStore
    
    llm = LLMGenerator()
    vector_store = ChromaVectorStore()
    
    # Test query
    test_query = "What's a good laptop for students under $800?"
    
    # Retrieve documents
    print(f"Query: {test_query}\n")
    docs = vector_store.search(test_query, top_k=5)
    
    # Generate answer
    result = llm.generate_answer_with_sources(test_query, docs)
    
    print("Answer:")
    print(result['answer'])
    print("\nSources used:")
    for source in result['sources']:
        print(f"  - {source['type']} (score: {source['score']:.3f})")