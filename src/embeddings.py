"""
Embedding generation for documents and queries
"""
import os
from typing import List
from openai import OpenAI
import yaml
from dotenv import load_dotenv

load_dotenv()


class EmbeddingGenerator:
    """Generate embeddings using OpenAI API"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.model = self.config['embeddings']['model']
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches"""
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
        
        return embeddings


if __name__ == "__main__":
    # Test embedding generation
    generator = EmbeddingGenerator()
    
    test_text = "What is the best laptop for gaming under $1500?"
    embedding = generator.generate_embedding(test_text)
    
    print(f"Generated embedding with dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")