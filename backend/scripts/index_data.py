#!/usr/bin/env python3
"""
Script to index PC component data to Algolia
Processes CSV files from datasets/csv/ and uploads to Algolia index
"""

import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from algoliasearch.search.client import SearchClientSync

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()

# Algolia configuration
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_ADMIN_API_KEY = os.getenv("ALGOLIA_ADMIN_API_KEY")
INDEX_NAME = "pc_components"

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / "datasets" / "csv"

# Component type mapping (CSV filename -> Component Type)
COMPONENT_TYPES = {
    "cpu.csv": "CPU",
    "motherboard.csv": "Motherboard",
    "video-card.csv": "GPU",
    "memory.csv": "Memory",
    "power-supply.csv": "Power Supply",
    "internal-hard-drive.csv": "Internal Hard Drive",
    "case.csv": "Case",
    "cpu-cooler.csv": "CPU Cooler",
    "case-fan.csv": "Case Fan",
    "monitor.csv": "Monitor",
    "keyboard.csv": "Keyboard",
    "mouse.csv": "Mouse",
    "headphones.csv": "Headphones",
    "speakers.csv": "Speakers",
}

def clean_price(price_str):
    """Convert price string to float"""
    if pd.isna(price_str) or price_str == '':
        return None
    try:
        return float(str(price_str).replace(',', '').replace('$', ''))
    except:
        return None

def extract_socket_from_cpu(row):
    """Extract socket type from CPU data"""
    # Common socket types
    name = str(row.get('name', '')).upper()
    
    if 'RYZEN' in name or 'AMD' in name:
        if '7' in name and ('7000' in name or '7900' in name or '7700' in name or '7600' in name):
            return 'AM5'
        elif '5000' in name or '5900' in name or '5800' in name or '5700' in name or '5600' in name:
            return 'AM4'
        elif any(x in name for x in ['3000', '2000', '1000']):
            return 'AM4'
        else:
            return 'AM4'  # Default for AMD
    
    elif 'INTEL' in name or 'CORE' in name or 'XEON' in name:
        if '14' in name or '13' in name or '12' in name:
            return 'LGA1700'
        elif '11' in name or '10' in name:
            return 'LGA1200'
        elif '9' in name or '8' in name:
            return 'LGA1151'
        else:
            return 'LGA1700'  # Default for modern Intel
    
    return None

def determine_performance_tier(row, component_type):
    """Determine performance tier based on price and specs"""
    price = row.get('price')
    
    if not price or pd.isna(price):
        return 'mid-range'
    
    if component_type == 'CPU':
        if price >= 400:
            return 'high-end'
        elif price >= 200:
            return 'mid-range'
        else:
            return 'budget'
    
    elif component_type == 'GPU':
        if price >= 800:
            return 'high-end'
        elif price >= 400:
            return 'mid-range'
        else:
            return 'budget'
    
    elif component_type == 'Motherboard':
        if price >= 300:
            return 'high-end'
        elif price >= 150:
            return 'mid-range'
        else:
            return 'budget'
    
    else:
        if price >= 200:
            return 'high-end'
        elif price >= 100:
            return 'mid-range'
        else:
            return 'budget'

def process_cpu_data(df):
    """Process CPU CSV data"""
    components = []
    
    for idx, row in df.iterrows():
        component = {
            "objectID": f"cpu_{idx}",
            "id": f"cpu_{idx}",
            "type": "CPU",
            "name": str(row.get('name', '')),
            "price": clean_price(row.get('price')),
            "brand": "AMD" if "AMD" in str(row.get('name', '')).upper() else "Intel" if "Intel" in str(row.get('name', '')).upper() else "Unknown",
            "specs": {
                "core_count": int(row['core_count']) if pd.notna(row.get('core_count')) else None,
                "core_clock": str(row.get('core_clock', '')),
                "boost_clock": str(row.get('boost_clock', '')),
                "microarchitecture": str(row.get('microarchitecture', '')),
                "tdp": int(row['tdp']) if pd.notna(row.get('tdp')) else None,
                "graphics": str(row.get('graphics', '')),
                "socket": extract_socket_from_cpu(row),
            },
        }
        
        # Add socket to top level for faceting
        component["socket"] = component["specs"]["socket"]
        component["performance_tier"] = determine_performance_tier(component, "CPU")
        
        components.append(component)
    
    return components

def process_motherboard_data(df):
    """Process Motherboard CSV data"""
    components = []
    
    for idx, row in df.iterrows():
        component = {
            "objectID": f"mb_{idx}",
            "id": f"mb_{idx}",
            "type": "Motherboard",
            "name": str(row.get('name', '')),
            "price": clean_price(row.get('price')),
            "brand": str(row.get('name', '').split()[0]),
            "specs": {
                "socket": str(row.get('socket', '')),
                "form_factor": str(row.get('form_factor', '')),
                "max_memory": int(row['max_memory']) if pd.notna(row.get('max_memory')) else None,
                "memory_slots": int(row['memory_slots']) if pd.notna(row.get('memory_slots')) else None,
                "color": str(row.get('color', '')),
            },
        }
        
        # Add facetable attributes to top level
        component["socket"] = component["specs"]["socket"]
        component["form_factor"] = component["specs"]["form_factor"]
        
        # Determine memory type from name
        name_upper = str(row.get('name', '')).upper()
        if 'DDR5' in name_upper:
            component["memory_type"] = "DDR5"
        elif 'DDR4' in name_upper:
            component["memory_type"] = "DDR4"
        else:
            # Default based on socket
            socket = component["socket"]
            if socket in ['AM5', 'LGA1700', 'LGA1851']:
                component["memory_type"] = "DDR5"
            else:
                component["memory_type"] = "DDR4"
        
        component["specs"]["memory_type"] = component["memory_type"]
        component["performance_tier"] = determine_performance_tier(component, "Motherboard")
        
        components.append(component)
    
    return components

def process_generic_data(df, component_type, type_key):
    """Process generic component CSV data"""
    components = []
    
    for idx, row in df.iterrows():
        # Convert row to dict and remove NaN values
        specs = {}
        for col in df.columns:
            if col not in ['name', 'price'] and pd.notna(row[col]):
                specs[col] = row[col]
        
        component = {
            "objectID": f"{type_key}_{idx}",
            "id": f"{type_key}_{idx}",
            "type": component_type,
            "name": str(row.get('name', '')),
            "price": clean_price(row.get('price')),
            "brand": str(row.get('name', '').split()[0]) if row.get('name') else "Unknown",
            "specs": specs,
        }
        
        component["performance_tier"] = determine_performance_tier(component, component_type)
        
        components.append(component)
    
    return components

def index_data_to_algolia():
    """Main function to index all data to Algolia"""
    
    if not ALGOLIA_APP_ID or not ALGOLIA_ADMIN_API_KEY:
        print("❌ Error: Algolia credentials not found in environment variables")
        print("Please set ALGOLIA_APP_ID and ALGOLIA_ADMIN_API_KEY in backend/.env")
        return False
    
    print(f"🚀 Starting data indexing to Algolia...")
    print(f"📊 Index: {INDEX_NAME}")
    print(f"📁 Data directory: {DATA_DIR}")
    
    # Initialize Algolia client (v4 API)
    client = SearchClientSync(ALGOLIA_APP_ID, ALGOLIA_ADMIN_API_KEY)
    
    # Clear existing index
    print("\n🗑️  Clearing existing index...")
    try:
        client.clear_objects(index_name=INDEX_NAME)
        print("✅ Index cleared")
    except Exception as e:
        print(f"⚠️  Warning: Could not clear index: {e}")
    
    all_components = []
    
    # Process each CSV file
    for filename, component_type in COMPONENT_TYPES.items():
        csv_path = DATA_DIR / filename
        
        if not csv_path.exists():
            print(f"⏭️  Skipping {filename} (file not found)")
            continue
        
        print(f"\n📄 Processing {filename} ({component_type})...")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"   Found {len(df)} rows")
            
            # Process based on type
            if component_type == "CPU":
                components = process_cpu_data(df)
            elif component_type == "Motherboard":
                components = process_motherboard_data(df)
            else:
                type_key = filename.replace('.csv', '').replace('-', '_')
                components = process_generic_data(df, component_type, type_key)
            
            all_components.extend(components)
            print(f"   ✅ Processed {len(components)} components")
            
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")
            continue
    
    # Upload to Algolia in batches
    print(f"\n📤 Uploading {len(all_components)} components to Algolia...")
    
    batch_size = 1000
    for i in range(0, len(all_components), batch_size):
        batch = all_components[i:i+batch_size]
        try:
            client.save_objects(index_name=INDEX_NAME, objects=batch)
            print(f"   ✅ Uploaded batch {i//batch_size + 1} ({len(batch)} components)")
        except Exception as e:
            print(f"   ❌ Error uploading batch: {e}")
    
    # Configure index settings
    print("\n⚙️  Configuring index settings...")
    try:
        settings = {
            "searchableAttributes": [
                "name",
                "brand",
                "type",
            ],
            "attributesForFaceting": [
                "type",
                "brand",
                "searchable(socket)",
                "searchable(memory_type)",
                "form_factor",
                "performance_tier",
            ],
            "customRanking": [
                "desc(performance_tier)",
                "asc(price)",
            ],
        }
        client.set_settings(index_name=INDEX_NAME, index_settings=settings)
        print("   ✅ Index settings configured")
    except Exception as e:
        print(f"   ❌ Error configuring settings: {e}")
    
    print(f"\n🎉 Indexing complete!")
    print(f"📊 Total components indexed: {len(all_components)}")
    print(f"🔍 Index name: {INDEX_NAME}")
    print(f"\nNext steps:")
    print(f"1. Test search: Visit your Algolia dashboard")
    print(f"2. Start backend: cd backend && uvicorn app.main:app --reload")
    print(f"3. Test API: http://localhost:5000/docs")
    
    return True

if __name__ == "__main__":
    success = index_data_to_algolia()
    sys.exit(0 if success else 1)
