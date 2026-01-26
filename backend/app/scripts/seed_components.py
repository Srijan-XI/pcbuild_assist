import hashlib
import csv
import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.services.algolia_service import algolia_service

# Map CSV filenames to component types
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
    """Generate stable ID using MD5"""
    m = hashlib.md5(name.encode('utf-8'))
    return f"{type.lower()}-{m.hexdigest()[:10]}"

def extract_brand(name: str) -> str:
    """Extract brand from component name"""
    if not name:
        return "Unknown"
    
    # Common brands mapping
    brands = [
        "AMD", "Intel", "NVIDIA", "ASUS", "MSI", "Gigabyte", "ASRock", 
        "Corsair", "G.Skill", "Samsung", "Western Digital", "Seagate", 
        "Crucial", "Kingston", "EVGA", "Thermaltake", "Cooler Master", 
        "NZXT", "Lian Li", "Fractal Design", "Be Quiet", "Noctua",
        "Deepcool", "Arctic", "Phanteks", "Seasonic", "Super Flower",
        "Zotac", "Sapphire", "PowerColor", "XFX", "PNY", "Inno3D",
        "TeamGroup", "ADATA", "Sabrent", "Lexar", "Silicon Power"
    ]
    
    name_upper = name.upper()
    for brand in brands:
        if brand.upper() in name_upper:
            # Handle special casing
            if brand.upper() == "ASUS": return "ASUS"
            if brand.upper() == "NVIDIA": return "NVIDIA"
            if brand.upper() == "MSI": return "MSI"
            if brand.upper() == "EVGA": return "EVGA"
            if brand.upper() == "NZXT": return "NZXT"
            if brand.upper() == "XFX": return "XFX"
            if brand.upper() == "PNY": return "PNY"
            if brand.upper() == "AMD": return "AMD"
            return brand
            
    return name.split(' ')[0]

def clean_price(price_str: str) -> float:
    """Convert price string to float"""
    if not price_str:
        return 0.0
    try:
        return float(price_str.replace('$', '').replace(',', ''))
    except ValueError:
        return 0.0

def process_file(filename: str, component_type: str) -> List[Dict[str, Any]]:
    file_path = DATASET_DIR / filename
    if not file_path.exists():
        print(f"Warning: File {file_path} not found.")
        return []

    items = []
    print(f"Processing {component_type} from {filename}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Basic fields
                name = row.get('name', '')
                price = clean_price(row.get('price', '0'))
                
                if not name:
                    continue
                    
                brand = extract_brand(name)
                
                # Create base component object
                component_id = generate_id(name, component_type)
                component = {
                    "objectID": component_id,
                    "id": component_id,
                    "type": component_type,
                    "name": name,
                    "brand": brand,
                    "price": price,
                    "image": row.get('image', ''),
                    "specs": {},
                }

                # Type-specific specs mapping
                if component_type == 'CPU':
                    component['specs'] = {
                        "core_count": int(row.get('core_count')) if row.get('core_count') and row.get('core_count').isdigit() else None,
                        "core_clock": row.get('core_clock'),
                        "boost_clock": row.get('boost_clock'),
                        "tdp": int(row.get('tdp')) if row.get('tdp') and row.get('tdp').isdigit() else None,
                        "graphics": row.get('graphics'),
                        "socket": "Unknown" 
                    }
                    if "AM5" in name: component['specs']['socket'] = "AM5"
                    elif "AM4" in name: component['specs']['socket'] = "AM4"
                    elif "LGA1700" in name or "Core i. 12" in name or "Core i. 13" in name or "Core i. 14" in name: component['specs']['socket'] = "LGA1700"
                    elif "LGA1200" in name or "Core i. 10" in name or "Core i. 11" in name: component['specs']['socket'] = "LGA1200"

                elif component_type == 'Motherboard':
                    component['specs'] = {
                        "socket": row.get('socket'),
                        "form_factor": row.get('form_factor'),
                        "max_memory": int(row.get('max_memory')) if row.get('max_memory') and row.get('max_memory').isdigit() else None,
                        "memory_slots": int(row.get('memory_slots')) if row.get('memory_slots') and row.get('memory_slots').isdigit() else None,
                        "memory_type": "DDR5" if "DDR5" in name or "AM5" in row.get('socket', '') or "LGA1851" in row.get('socket', '') else "DDR4" 
                    }
                    if "DDR4" in name: component['specs']['memory_type'] = "DDR4"
                    elif "DDR5" in name: component['specs']['memory_type'] = "DDR5"

                elif component_type == 'GPU':
                    component['specs'] = {
                        "chipset": row.get('chipset', ''),
                        "memory": row.get('memory', ''),
                        "core_clock": row.get('core_clock', ''),
                        "boost_clock": row.get('boost_clock', ''),
                    }
                    if "GeForce" in name: component['specs']['chipset'] = "NVIDIA"
                    elif "Radeon" in name: component['specs']['chipset'] = "AMD"
                    elif "Arc" in name: component['specs']['chipset'] = "Intel"

                elif component_type == 'RAM':
                    component['specs'] = {
                        "speed": row.get('speed', ''),
                        "modules": row.get('modules', ''),
                        "price_per_gb": row.get('price_per_gb', ''),
                        "latency": row.get('cas_latency', '')
                    }
                    if "DDR5" in name or "DDR5" in str(row.get('speed', '')):
                        component['type'] = 'RAM'
                        component['specs']['type'] = 'DDR5'
                    elif "DDR4" in name or "DDR4" in str(row.get('speed', '')):
                        component['specs']['type'] = 'DDR4'

                elif component_type == 'Storage':
                    component['specs'] = {
                        "capacity": row.get('capacity', ''),
                        "price_per_gb": row.get('price_per_gb', ''),
                        "type": row.get('type', ''),
                        "cache": row.get('cache', ''),
                        "form_factor": row.get('form_factor', '')
                    }

                elif component_type == 'PSU':
                    component['specs'] = {
                        "wattage": row.get('wattage', ''),
                        "efficiency": row.get('efficiency', ''), 
                        "modular": row.get('modular', '')
                    }
                    if component['specs']['wattage']:
                        try:
                            w = component['specs']['wattage'].lower().replace('w', '')
                            component['specs']['wattage'] = int(w)
                        except: pass

                elif component_type == 'Case':
                    component['specs'] = {
                        "type": row.get('type', ''),
                        "color": row.get('color', ''),
                        "side_panel": row.get('side_panel', '')
                    }
                
                items.append(component)
                
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        
    return items

def main():
    print("Starting data seeding...")
    
    # Clear existing index
    print("Clearing existing index...")
    algolia_service.clear_index()

    # Configure index first
    print("Configuring Algolia index settings...")
    algolia_service.configure_index_settings()
    
    all_components = []
    
    for filename, component_type in COMPONENT_FILES.items():
        components = process_file(filename, component_type)
        all_components.extend(components)
        print(f"Found {len(components)} {component_type}s")
        
    if not all_components:
        print("No components found to seed.")
        return
        
    print(f"Total components to index: {len(all_components)}")
    
    # Index in batches of 1000
    batch_size = 1000
    for i in range(0, len(all_components), batch_size):
        batch = all_components[i:i+batch_size]
        print(f"Indexing batch {i//batch_size + 1} ({len(batch)} items)...")
        result = algolia_service.index_components(batch)
        if result.get('success'):
            print("Batch indexed successfully.")
        else:
            print(f"Error indexing batch: {result.get('error')}")
            
    print("Seeding completed!")

if __name__ == "__main__":
    main()
