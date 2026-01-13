"""
Download Amazon product metadata and reviews
"""
import os
import requests
from tqdm import tqdm
import gzip
import shutil

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

DATASETS = {
    "products": {
        "url": "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/metaFiles2/meta_Electronics.json.gz",
        "filename": "meta_Electronics.json.gz",
        "extracted": "products_electronics.json"
    },
    "reviews": {
        "url": "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/categoryFiles/Electronics.json.gz",
        "filename": "Electronics_reviews.json.gz",
        "extracted": "reviews_electronics.json"
    }
}

def download_file(url, filename):
    """Download file with progress bar"""
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"✓ {filename} already exists, skipping download")
        return filepath
    
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, 'wb') as f, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        desc=filename
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
    
    print(f"✓ Downloaded {filename}")
    return filepath

def extract_gz(gz_path, output_path):
    """Extract gzipped file"""
    if os.path.exists(output_path):
        print(f"✓ {output_path} already exists, skipping extraction")
        return
    
    print(f"Extracting {os.path.basename(gz_path)}...")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"✓ Extracted to {output_path}")

def sample_file(input_path, output_path, num_lines):
    """Create a sample of the dataset"""
    if os.path.exists(output_path):
        print(f"✓ {output_path} already exists, skipping sampling")
        return
    
    print(f"Creating sample with {num_lines} lines...")
    with open(input_path, 'r') as f_in:
        with open(output_path, 'w') as f_out:
            for i, line in enumerate(f_in):
                if i >= num_lines:
                    break
                f_out.write(line)
    print(f"✓ Created sample at {output_path}")

def main():
    print("=" * 60)
    print("ShopAssist RAG - Data Download Script")
    print("=" * 60)
    
    # Download products
    print("\n1. Downloading Product Metadata...")
    products_gz = download_file(
        DATASETS["products"]["url"],
        DATASETS["products"]["filename"]
    )
    products_path = os.path.join(DATA_DIR, DATASETS["products"]["extracted"])
    extract_gz(products_gz, products_path)
    
    # Create product sample (50K products)
    sample_file(
        products_path,
        os.path.join(DATA_DIR, "products_50k.json"),
        50000
    )
    
    # Download reviews
    print("\n2. Downloading Reviews...")
    reviews_gz = download_file(
        DATASETS["reviews"]["url"],
        DATASETS["reviews"]["filename"]
    )
    reviews_path = os.path.join(DATA_DIR, DATASETS["reviews"]["extracted"])
    extract_gz(reviews_gz, reviews_path)
    
    # Create review sample (100K reviews)
    sample_file(
        reviews_path,
        os.path.join(DATA_DIR, "reviews_100k.json"),
        100000
    )
    
    print("\n" + "=" * 60)
    print("✓ Data download complete!")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  - {os.path.join(DATA_DIR, 'products_50k.json')}")
    print(f"  - {os.path.join(DATA_DIR, 'reviews_100k.json')}")

if __name__ == "__main__":
    main()