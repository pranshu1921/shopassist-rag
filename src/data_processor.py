"""
Data processing pipeline for products, reviews, and policies
"""
import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass
import yaml


@dataclass
class Document:
    """Represents a processed document for RAG"""
    content: str
    metadata: Dict[str, Any]
    doc_type: str  # 'product', 'review', or 'policy'
    doc_id: str


class DataProcessor:
    """Process raw data into RAG-ready documents"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.chunk_size = self.config['data']['chunk_size']
        self.chunk_overlap = self.config['data']['chunk_overlap']
    
    def load_products(self, filepath: str, limit: int = None) -> List[Dict]:
        """Load product metadata from JSON file"""
        products = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                try:
                    product = json.loads(line)
                    products.append(product)
                except json.JSONDecodeError:
                    continue
        return products
    
    def load_reviews(self, filepath: str, limit: int = None) -> List[Dict]:
        """Load reviews from JSON file"""
        reviews = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                try:
                    review = json.loads(line)
                    reviews.append(review)
                except json.JSONDecodeError:
                    continue
        return reviews
    
    def load_policies(self, directory: str) -> List[Dict]:
        """Load policy markdown files"""
        policies = []
        policy_files = [f for f in os.listdir(directory) if f.endswith('.md')]
        
        for filename in policy_files:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                content = f.read()
                policies.append({
                    'filename': filename,
                    'content': content,
                    'title': filename.replace('_', ' ').replace('.md', '').title()
                })
        return policies
    
    def process_product(self, product: Dict) -> Document:
        """Convert product to RAG document"""
        # Extract key fields
        title = product.get('title', 'Unknown Product')
        asin = product.get('asin', 'unknown')
        description = product.get('description', [''])
        if isinstance(description, list):
            description = ' '.join(description)
        
        features = product.get('feature', [])
        if isinstance(features, list):
            features_text = '\n'.join([f"- {f}" for f in features])
        else:
            features_text = ''
        
        category = product.get('category', [])
        if isinstance(category, list):
            category_text = ' > '.join(category)
        else:
            category_text = str(category)
        
        price = product.get('price', 'N/A')
        brand = product.get('brand', 'Unknown')
        
        # Build content
        content = f"""Product: {title}

Brand: {brand}
Price: {price}
Category: {category_text}

Description:
{description}

Key Features:
{features_text}
"""
        
        metadata = {
            'asin': asin,
            'title': title,
            'brand': brand,
            'price': price,
            'category': category_text
        }
        
        return Document(
            content=content.strip(),
            metadata=metadata,
            doc_type='product',
            doc_id=f"product_{asin}"
        )
    
    def process_review(self, review: Dict) -> Document:
        """Convert review to RAG document"""
        asin = review.get('asin', 'unknown')
        reviewer = review.get('reviewerName', 'Anonymous')
        rating = review.get('overall', 0)
        summary = review.get('summary', '')
        text = review.get('reviewText', '')
        
        # Build content
        content = f"""Customer Review for Product {asin}

Rating: {rating}/5 stars
Reviewer: {reviewer}

Title: {summary}

Review:
{text}
"""
        
        metadata = {
            'asin': asin,
            'rating': rating,
            'reviewer': reviewer,
            'summary': summary
        }
        
        return Document(
            content=content.strip(),
            metadata=metadata,
            doc_type='review',
            doc_id=f"review_{asin}_{hash(text) % 10000}"
        )
    
    def process_policy(self, policy: Dict) -> Document:
        """Convert policy to RAG document"""
        title = policy['title']
        content = policy['content']
        filename = policy['filename']
        
        metadata = {
            'title': title,
            'filename': filename,
            'doc_type': 'policy'
        }
        
        return Document(
            content=content,
            metadata=metadata,
            doc_type='policy',
            doc_id=f"policy_{filename.replace('.md', '')}"
        )
    
    def chunk_document(self, doc: Document) -> List[Document]:
        """Split long documents into chunks"""
        content = doc.content
        
        # If document is short enough, return as is
        if len(content) <= self.chunk_size:
            return [doc]
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(content):
            end = start + self.chunk_size
            chunk_text = content[start:end]
            
            # Create new document for chunk
            chunk_metadata = doc.metadata.copy()
            chunk_metadata['chunk_id'] = chunk_id
            chunk_metadata['is_chunk'] = True
            
            chunk_doc = Document(
                content=chunk_text,
                metadata=chunk_metadata,
                doc_type=doc.doc_type,
                doc_id=f"{doc.doc_id}_chunk_{chunk_id}"
            )
            chunks.append(chunk_doc)
            
            # Move start pointer with overlap
            start = end - self.chunk_overlap
            chunk_id += 1
        
        return chunks
    
    def process_all(self, data_dir: str = "data/raw") -> List[Document]:
        """Process all data sources"""
        documents = []
        
        print("Processing products...")
        products = self.load_products(
            os.path.join(data_dir, "products_50k.json"),
            limit=self.config['data']['products_limit']
        )
        for product in products:
            doc = self.process_product(product)
            chunks = self.chunk_document(doc)
            documents.extend(chunks)
        print(f"  ✓ Processed {len(products)} products")
        
        print("Processing reviews...")
        reviews = self.load_reviews(
            os.path.join(data_dir, "reviews_100k.json"),
            limit=self.config['data']['reviews_limit']
        )
        for review in reviews:
            doc = self.process_review(review)
            chunks = self.chunk_document(doc)
            documents.extend(chunks)
        print(f"  ✓ Processed {len(reviews)} reviews")
        
        print("Processing policies...")
        policies = self.load_policies(data_dir)
        for policy in policies:
            doc = self.process_policy(policy)
            chunks = self.chunk_document(doc)
            documents.extend(chunks)
        print(f"  ✓ Processed {len(policies)} policies")
        
        return documents
    
    def save_processed_data(self, documents: List[Document], output_path: str):
        """Save processed documents to JSON"""
        data = []
        for doc in documents:
            data.append({
                'content': doc.content,
                'metadata': doc.metadata,
                'doc_type': doc.doc_type,
                'doc_id': doc.doc_id
            })
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Saved {len(documents)} documents to {output_path}")


if __name__ == "__main__":
    processor = DataProcessor()
    docs = processor.process_all()
    
    os.makedirs("data/processed", exist_ok=True)
    processor.save_processed_data(docs, "data/processed/documents.json")
    
    print(f"\nTotal documents: {len(docs)}")
    print(f"  Products: {sum(1 for d in docs if d.doc_type == 'product')}")
    print(f"  Reviews: {sum(1 for d in docs if d.doc_type == 'review')}")
    print(f"  Policies: {sum(1 for d in docs if d.doc_type == 'policy')}")