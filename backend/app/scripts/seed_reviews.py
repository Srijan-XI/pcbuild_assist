import hashlib
import pandas as pd
import os
import sys
import csv
from pathlib import Path
from typing import List, Dict, Any

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.services.algolia_service import algolia_service

# Reuse configuration
COMPONENT_FILES = {
    'cpu.csv': 'CPU',
    'motherboard.csv': 'Motherboard',
    'video-card.csv': 'GPU',
    'memory.csv': 'RAM',
    'internal-hard-drive.csv': 'Storage',
    'power-supply.csv': 'PSU',
    'case.csv': 'Case',
    'cpu-cooler.csv': 'CPU Cooler'
}

DATASET_DIR = Path(__file__).resolve().parent.parent.parent.parent / 'datasets' / 'csv'

def generate_id(name: str, type: str) -> str:
    """Generate stable ID using MD5 - MUST MATCH seed_components.py"""
    m = hashlib.md5(name.encode('utf-8'))
    return f"{type.lower()}-{m.hexdigest()[:10]}"

def load_component_map() -> Dict[str, Dict]:
    """Load all component names and IDs"""
    print("Loading component map...")
    comp_map = {} # Name -> {id, type}
    
    for filename, component_type in COMPONENT_FILES.items():
        file_path = DATASET_DIR / filename
        if not file_path.exists(): continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get('name', '')
                    if name:
                        comp_id = generate_id(name, component_type)
                        # Store lower case name for easier matching
                        comp_map[name] = {"id": comp_id, "type": component_type, "real_name": name}
        except Exception: 
            pass
            
    print(f"Loaded {len(comp_map)} components to match against.")
    return comp_map

def main():
    print("Starting review seeding...")
    
    # 1. Load Reviews
    try:
        print("Loading reviews from HuggingFace...")
        df = pd.read_parquet("hf://datasets/argilla/pc-components-reviews/data/train-00000-of-00001.parquet")
        reviews = df.to_dict(orient='records')
        print(f"Loaded {len(reviews)} reviews.")
    except Exception as e:
        print(f"Error loading reviews: {e}")
        return

    # 2. Load matched components
    comp_map = load_component_map()
    
    # Sort names by length descending to match longest specific name first
    # e.g. match "Ryzen 7 5800X" before "Ryzen 7"
    sorted_names = sorted(comp_map.keys(), key=len, reverse=True)
    
    # 3. Match reviews
    updates = {} # ID -> list of reviews
    
    matched_count = 0
    
    for review in reviews:
        text = review.get('text', '')
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            continue
        
        # Simple inclusion check (case insensitive?) 
        # The dataset seems to have proper casing "AMD Ryzen...", let's try case sensitive first or relaxed
        # Let's do case insensitive for better hit rate
        text_lower = text.lower()
        
        match_found = None
        for name in sorted_names:
            if name.lower() in text_lower:
                match_found = name
                break # taking longest match
        
        if match_found:
            comp_data = comp_map[match_found]
            comp_id = comp_data['id']
            
            if comp_id not in updates:
                updates[comp_id] = []
                
            updates[comp_id].append({
                "text": text.strip(),
                "sentiment": review.get('sentiment'),
                "author_age": review.get('age_group'),
                "author_expertise": review.get('expertise'),
                "labels": review.get('labels')
            })
            matched_count += 1
            
    print(f"Matched {matched_count} reviews to {len(updates)} distinct components.")
    
    # 4. Push to Algolia
    if not updates:
        print("No matches found to update.")
        return

    algolia_payload = []
    for comp_id, review_list in updates.items():
        # We append to 'reviews' attribute. 
        # Note: partial_update replaces the attribute. Since we started fresh, we can just set it.
        # If we wanted to append, we'd need to use 'Add' operation or read first.
        # Assuming fresh start here.
        algolia_payload.append({
            "objectID": comp_id,
            "reviews": review_list,
            "review_count": len(review_list),
            # Maybe calculate average sentiment score?
        })
        
    print(f"Sending {len(algolia_payload)} updates to Algolia...")
    
    # Batch update
    batch_size = 1000
    for i in range(0, len(algolia_payload), batch_size):
        batch = algolia_payload[i:i+batch_size]
        print(f"Updating batch {i//batch_size + 1}...")
        res = algolia_service.partial_update_components(batch)
        if res.get('success'):
            print("Batch updated.")
        else:
            print(f"Error: {res.get('error')}")

if __name__ == "__main__":
    main()
