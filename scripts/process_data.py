"""
Script to run data processing pipeline
"""
import sys
sys.path.append('.')

from src.data_processor import DataProcessor

def main():
    print("=" * 60)
    print("ShopAssist RAG - Data Processing")
    print("=" * 60)
    
    processor = DataProcessor()
    
    print("\nProcessing raw data...")
    documents = processor.process_all("data/raw")
    
    print("\nSaving processed documents...")
    processor.save_processed_data(documents, "data/processed/documents.json")
    
    print("\n" + "=" * 60)
    print("✓ Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()