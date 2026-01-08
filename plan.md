# Project Plan: PCBuild Assist with Algolia Integration

## Overview
Build a smart PC component builder that uses Algolia Agent Studio to proactively suggest compatible components based on user selections, demonstrating intelligent data retrieval without requiring conversational interaction.

## Phase 1: Setup & Foundation (Days 1-2)

### 1.1 Algolia Account Setup
- [ ] Visit [algolia.com](https://algolia.com) and sign up for a free account
- [ ] Navigate to Dashboard and create a new Algolia application
- [ ] Access API keys:
  - **Application ID**: Unique identifier for your app
  - **Search-Only API Key**: For frontend queries (read-only)
  - **Admin API Key**: For backend indexing operations (keep secure, never expose to client)
- [ ] Note down Region: `us` or `eu` (affects endpoint URLs)
- [ ] Verify Free Build Plan limitations:
  - 10,000 records per index
  - 1,000,000 operations per month
  - Sufficient for this project
- [ ] Save credentials securely in environment variables

### 1.2 Development Environment Setup
- [ ] Install Node.js (LTS version) or Python 3.9+
- [ ] Install Git for version control
- [ ] Install code editor (VS Code recommended)
- [ ] Set up package managers:
  - For Node: npm or yarn
  - For Python: pip and virtual environment (venv)
- [ ] Install Docker (optional, for local PostgreSQL/MongoDB)
- [ ] Install Postman or similar for API testing
- [ ] Set up environment file template (.env):
  ```
  ALGOLIA_APP_ID=your_app_id
  ALGOLIA_SEARCH_API_KEY=your_search_key
  ALGOLIA_ADMIN_API_KEY=your_admin_key
  DATABASE_URL=your_db_url
  BACKEND_PORT=5000
  FRONTEND_PORT=3000
  ```

### 1.3 Project Repository Initialization
- [ ] Create GitHub/GitLab repository
- [ ] Clone to local machine
- [ ] Create `.gitignore` file to exclude:
  - `node_modules/`, `__pycache__/`
  - `.env` (environment variables)
  - `*.log`, `.DS_Store`
  - IDE-specific files (`.vscode/`, `.idea/`)
- [ ] Create initial commit with basic structure

### 1.4 Project Structure Creation
```
project-root/
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js          # or webpack.config.js
├── backend/                     # FastAPI/Express server
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── __init__.py
│   │   └── main.py             # or server.js
│   ├── data/
│   │   └── components.json     # Raw component data
│   ├── requirements.txt        # or package.json
│   └── .env.example
├── docs/                        # Documentation
│   ├── README.md
│   └── API.md
├── .gitignore
└── plan.md
```

### 1.5 Backend Framework Setup
**Option A: Python FastAPI**
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies:
  ```
  pip install fastapi uvicorn algoliasearch python-dotenv sqlalchemy psycopg2-binary
  ```
- [ ] Create main.py with basic FastAPI app structure
- [ ] Set up CORS for frontend communication

**Option B: Node.js Express**
- [ ] Initialize npm: `npm init -y`
- [ ] Install dependencies:
  ```
  npm install express algoliasearch dotenv cors axios
  ```
- [ ] Create server.js with basic Express setup

### 1.6 Frontend Framework Setup
- [ ] Initialize React project with Vite: `npm create vite@latest frontend -- --template react`
- [ ] Install dependencies:
  ```
  npm install react react-dom algoliasearch
  npm install -D tailwindcss postcss autoprefixer
  ```
- [ ] Configure Tailwind CSS for styling (optional but recommended)
- [ ] Create basic folder structure for components and pages
- [ ] Set up API service file for backend communication

### 1.7 Database Setup (Local)
- [ ] Install PostgreSQL or use MongoDB locally
- [ ] Create database: `createdb pc_builder`
- [ ] Set connection string in `.env`
- [ ] Prepare database connection code (will be used in Phase 2)
- [ ] Optional: Use Docker for database:
  ```
  docker run --name postgres-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
  ```

### 1.8 Testing Setup
- [ ] Install testing framework:
  - Python: `pip install pytest`
  - Node: `npm install -D jest`
- [ ] Create test directory structure: `tests/` or `__tests__/`
- [ ] Write first placeholder test to verify setup

## Phase 2: Data Preparation (Days 3-4)

### 2.1 Define PC Component Database Schema

**CPU Schema Example:**
```json
{
  "id": "cpu_001",
  "name": "Intel Core i9-13900K",
  "brand": "Intel",
  "model": "i9-13900K",
  "socket": "LGA1700",
  "cores": 24,
  "threads": 32,
  "base_clock": "3.0 GHz",
  "boost_clock": "5.8 GHz",
  "tdp": 253,
  "price": 589.99,
  "release_year": 2022,
  "performance_tier": "high-end",
  "compatible_sockets": ["LGA1700"],
  "power_requirement": 250,
  "segment": "gaming,streaming,workstation"
}
```

**GPU Schema Example:**
```json
{
  "id": "gpu_001",
  "name": "NVIDIA RTX 4090",
  "brand": "NVIDIA",
  "chip": "AD102",
  "memory_gb": 24,
  "memory_type": "GDDR6X",
  "boost_clock": "2.5 GHz",
  "tdp": 450,
  "price": 1599.99,
  "release_year": 2022,
  "performance_tier": "high-end",
  "min_psu": 850,
  "min_power_pins": "12VHPWR",
  "compatibility": "PCIe 4.0",
  "segment": "gaming,4k,professional"
}
```

**Motherboard Schema Example:**
```json
{
  "id": "mb_001",
  "name": "ASUS ROG Maximus Z790",
  "brand": "ASUS",
  "chipset": "Z790",
  "socket": "LGA1700",
  "form_factor": "ATX",
  "pcie_version": "5.0",
  "memory_type": "DDR5",
  "memory_slots": 2,
  "memory_max": 192,
  "price": 389.99,
  "features": ["WiFi6E", "Thunderbolt4", "USB-C"],
  "power_delivery": "22+2+1 Phase",
  "vrm_quality": "high",
  "compatibility": {
    "cpu_socket": "LGA1700",
    "gpu_pcie": "5.0",
    "ram_type": "DDR5"
  }
}
```

**RAM Schema Example:**
```json
{
  "id": "ram_001",
  "name": "Corsair Vengeance DDR5 32GB",
  "brand": "Corsair",
  "capacity_gb": 32,
  "speed": "6000MHz",
  "type": "DDR5",
  "voltage": 1.40,
  "cas_latency": 30,
  "price": 129.99,
  "form_factor": "DIMM",
  "compatibility": {
    "memory_type": "DDR5",
    "speed_range": ["5200-6400"]
  }
}
```

**PSU Schema Example:**
```json
{
  "id": "psu_001",
  "name": "Corsair RM1000x Gold",
  "brand": "Corsair",
  "wattage": 1000,
  "efficiency": "Gold",
  "form_factor": "ATX",
  "modular": "full-modular",
  "price": 189.99,
  "connectors": {
    "24pin_atx": 1,
    "8pin_cpu": 2,
    "8pin_pcie": 4,
    "6pin_pcie": 0
  }
}
```

**Storage Schema Example:**
```json
{
  "id": "storage_001",
  "name": "Samsung 990 Pro 2TB",
  "brand": "Samsung",
  "type": "NVMe SSD",
  "capacity_gb": 2048,
  "interface": "PCIe 4.0",
  "form_factor": "M.2",
  "speed_read": 7100,
  "speed_write": 6000,
  "price": 199.99,
  "compatibility": {
    "interface_type": "NVMe",
    "form_factor": "M.2"
  }
}
```

### 2.2 Create Compatibility Rules and Constraints

**Critical Compatibility Rules:**
1. **CPU-Motherboard Compatibility**
   - CPU socket MUST match motherboard socket
   - Example: Intel i9-13900K (LGA1700) → Motherboard with LGA1700
   - Rule: `cpu.socket == motherboard.socket`

2. **RAM-Motherboard Compatibility**
   - RAM type MUST match motherboard memory type (DDR4 vs DDR5)
   - RAM speed MUST be within motherboard's supported range
   - Motherboard must have available DIMM slots
   - Example: DDR5 RAM (6000MHz) → Z790 Motherboard supports DDR5
   - Rule: `ram.type == motherboard.memory_type && ram.speed <= motherboard.max_speed`

3. **GPU-Motherboard Compatibility**
   - Motherboard MUST have available PCIe slot
   - Motherboard PCIe version should match or exceed GPU requirements
   - Rule: `motherboard.pcie_version >= gpu.pcie_version`

4. **GPU-PSU Compatibility**
   - PSU wattage MUST exceed total system power requirement
   - GPU power connectors MUST be available on PSU
   - Rule: `psu.wattage >= (cpu.tdp + gpu.tdp + system_overhead)`

5. **CPU-PSU Compatibility**
   - PSU must provide adequate 8-pin/4-pin CPU connectors
   - Rule: `psu.8pin_cpu_connectors >= cpu.power_pins_required`

6. **Motherboard Form Factor Compatibility**
   - Motherboard form factor MUST fit in case
   - (Not included in this phase, handled in case selection)

**Storage Compatibility:**
- NVMe SSDs only fit M.2 slots on motherboard
- SATA SSDs need SATA ports and cables
- Rule: `storage.form_factor == motherboard.m2_compatible`

**Performance-Based Rules:**
- CPU tier + GPU tier should be balanced (avoid bottlenecks)
- RAM capacity: Minimum 16GB recommended; 32GB+ for streaming/3D rendering
- PSU efficiency rating recommendation: Gold+ for 80% efficiency

### 2.3 Prepare Component Inventory Data

**Step 1: Data Collection**
- [ ] Research current market components (2024-2025)
- [ ] Collect from sources:
  - PCPartPicker API (if available)
  - Amazon/Newegg product data
  - Manufacturer specifications
  - Tech review sites (TechPowerUp, Tom's Hardware)
- [ ] Create `backend/data/components.json` with ~200-500 components initially

**Step 2: Data Format Normalization**
- [ ] Standardize all prices to USD
- [ ] Convert all speeds/frequencies to MHz/GHz
- [ ] Normalize power consumption to watts (TDP)
- [ ] Standardize date formats (YYYY-MM-DD)
- [ ] Create unique IDs for each component (component_type_serial)

**Step 3: Data Validation**
- [ ] Verify no missing required fields
- [ ] Check for data type consistency (numbers as numbers, strings as strings)
- [ ] Validate price ranges are reasonable
- [ ] Ensure compatibility data is consistent
- [ ] Remove duplicates

**Example Components CSV → JSON conversion:**
- [ ] Parse CSV file from PCPartPicker export
- [ ] Map columns to schema fields
- [ ] Validate and enrich with additional metadata
- [ ] Save as `components.json`

### 2.4 Configure Algolia Index

**Step 1: Create Index in Algolia Dashboard**
- [ ] Log into Algolia Dashboard
- [ ] Go to "Indices" → "Create Index"
- [ ] Name index: `pc_components` (or similar)
- [ ] Region: Choose closest to your users

**Step 2: Configure Searchable Attributes**
- [ ] Make these attributes searchable:
  ```
  - name (highest priority)
  - brand
  - model
  - chipset
  - segment
  - features
  ```
- [ ] Set attribute ranking:
  1. `name` - Product name (most important)
  2. `brand` - Brand name
  3. `model` - Model number
  4. `segment` - Category/use case

**Step 3: Configure Facets (for filtering)**
Facets allow users to filter results. Configure these:
- [ ] **Exact facets** (fixed values):
  - `type` (CPU, GPU, RAM, MB, PSU, Storage)
  - `brand`
  - `socket` (CPU/Motherboard compatibility)
  - `memory_type` (DDR4/DDR5)
  - `form_factor`
  
- [ ] **Numeric facets** (range filtering):
  - `price` (0-3000)
  - `cores` (CPU)
  - `memory_gb` (RAM/GPU)
  - `tdp` (power consumption)
  - `release_year`

**Step 4: Set Up Ranking**
- [ ] Custom ranking attributes:
  1. `performance_tier` (high-end, mid-range, budget)
  2. `release_year` (newer first)
  3. `popularity` (optional, if available)
  4. `price` (ascending by default)

**Step 5: Configure Highlighting & Snippets**
- [ ] Enable highlighting on searchable attributes
- [ ] Set snippet length to 100 characters
- [ ] Highlight matching terms in results

**Step 6: Enable Advanced Features**
- [ ] Synonyms: Map alternate names (e.g., "RTX 4090" → "Ada GPU")
- [ ] Typo tolerance: Allow "i9-13900k" to match "i9 13900K"
- [ ] Deduplication: Handle duplicate entries
- [ ] Pagination: Set hits per page to 20

**Step 7: Configure Analytics & Insights**
- [ ] Enable search analytics (tracks popular searches)
- [ ] Enable click analytics (tracks user interactions)
- [ ] These insights inform recommendations later

### 2.5 Implement Data Sync Mechanism

**Step 1: Create Backend Data Sync Service**
```python
# backend/app/services/algolia_sync.py
from algoliasearch.search_client import SearchClient

class AlgoliaSync:
    def __init__(self, app_id, admin_key):
        self.client = SearchClient.create(app_id, admin_key)
        self.index = self.client.init_index('pc_components')
    
    def sync_components(self, components_data):
        """
        Sync component data to Algolia index
        - components_data: List of dicts with component info
        """
        # Add objectID (required by Algolia)
        for component in components_data:
            component['objectID'] = component['id']
        
        # Batch upload
        response = self.index.save_objects(components_data)
        return response
    
    def update_single_component(self, component_id, updates):
        """Update a single component"""
        self.index.partial_update_object({
            'objectID': component_id,
            **updates
        })
    
    def delete_component(self, component_id):
        """Remove component from index"""
        self.index.delete_object(component_id)
```

**Step 2: Initial Data Upload**
- [ ] Load component data from `backend/data/components.json`
- [ ] Validate all required fields
- [ ] Call `sync_components()` to upload to Algolia
- [ ] Verify in Algolia Dashboard that records appear

**Step 3: Incremental Sync Strategy**
Option A: **Scheduled Full Sync** (Daily)
- [ ] Set cron job to re-sync all data daily
- [ ] Useful for market price changes

Option B: **Event-Based Partial Sync** (Real-time)
- [ ] Trigger sync when prices/availability change
- [ ] Update only affected components
- [ ] More efficient for frequently changing data

Option C: **Manual Sync** (For this project)
- [ ] Admin endpoint to trigger sync manually
- [ ] Sufficient for demo purposes

**Step 4: Error Handling & Logging**
- [ ] Log all sync operations
- [ ] Catch and handle Algolia API errors
- [ ] Retry failed uploads (exponential backoff)
- [ ] Track sync success/failure rates

**Step 5: Verify Sync Success**
- [ ] Check Algolia Dashboard for record count
- [ ] Confirm all components are searchable
- [ ] Test sample queries to verify data retrieval
- [ ] Validate facet counts match data

## Phase 3: Backend Development (Days 5-7)

### 3.1 Backend API Setup

**Create Main Application Structure (Python FastAPI)**
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="PCBuild Assist API",
    description="Smart PC component builder with Algolia integration",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from app.routes import components, compatibility, suggestions

app.include_router(components.router, prefix="/api/components", tags=["Components"])
app.include_router(compatibility.router, prefix="/api/compatibility", tags=["Compatibility"])
app.include_router(suggestions.router, prefix="/api/suggestions", tags=["Suggestions"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

**Create Models for Type Safety**
```python
# backend/app/models/component.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class Component(BaseModel):
    id: str
    name: str
    brand: str
    type: str  # CPU, GPU, RAM, MB, PSU, Storage
    price: float
    specs: Dict
    compatibility: Dict

class ComponentResponse(Component):
    search_score: Optional[float] = None

class SearchRequest(BaseModel):
    query: str
    component_type: Optional[str] = None
    max_price: Optional[float] = None
    min_performance_tier: Optional[str] = None
    filters: Optional[Dict] = {}
    limit: int = 20
    offset: int = 0
```

### 3.2 Implement Algolia SDK Integration

**Create Algolia Service Layer**
```python
# backend/app/services/algolia_service.py
from algoliasearch.search_client import SearchClient
from algoliasearch.search_index import SearchIndex
from typing import List, Dict, Any
import os

class AlgoliaService:
    def __init__(self):
        self.app_id = os.getenv("ALGOLIA_APP_ID")
        self.search_api_key = os.getenv("ALGOLIA_SEARCH_API_KEY")
        self.admin_api_key = os.getenv("ALGOLIA_ADMIN_API_KEY")
        
        self.client = SearchClient.create(self.app_id, self.admin_api_key)
        self.index = self.client.init_index("pc_components")
        self.search_client = SearchClient.create(self.app_id, self.search_api_key)
        self.search_index = self.search_client.init_index("pc_components")
    
    def search_components(self, query: str, filters: Dict = None, limit: int = 20) -> List[Dict]:
        """
        Search components using Algolia
        - query: Search term (component name, brand, etc.)
        - filters: Dictionary with filter criteria
        - limit: Maximum results
        """
        search_params = {
            "query": query,
            "hitsPerPage": limit,
            "analytics": True,  # Track searches for insights
        }
        
        # Add Algolia facet filters if provided
        if filters:
            facet_filters = []
            for key, value in filters.items():
                if isinstance(value, list):
                    facet_filters.append([f"{key}:{v}" for v in value])
                else:
                    facet_filters.append(f"{key}:{value}")
            search_params["facetFilters"] = facet_filters
        
        response = self.search_index.search(search_params)
        return response.get("hits", [])
    
    def search_by_type(self, component_type: str, filters: Dict = None) -> List[Dict]:
        """Search components by type (CPU, GPU, etc.)"""
        search_params = {
            "query": "",
            "facetFilters": [f"type:{component_type}"],
            "hitsPerPage": 100,
        }
        
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    search_params["facetFilters"].extend([f"{key}:{v}" for v in value])
        
        response = self.search_index.search(search_params)
        return response.get("hits", [])
    
    def get_facets(self, component_type: str = None) -> Dict:
        """Get available facet values for filtering"""
        search_params = {
            "query": "",
            "facets": ["brand", "performance_tier", "socket", "memory_type"],
            "hitsPerPage": 0,  # Don't return results, only facets
        }
        
        if component_type:
            search_params["facetFilters"] = [f"type:{component_type}"]
        
        response = self.search_index.search(search_params)
        return response.get("facets", {})

# Create singleton instance
algolia_service = AlgoliaService()
```

### 3.3 Create Component Search Endpoints

**Route: Search Components**
```python
# backend/app/routes/components.py
from fastapi import APIRouter, Query
from typing import Optional, Dict
from app.models.component import SearchRequest, ComponentResponse
from app.services.algolia_service import algolia_service

router = APIRouter()

@router.get("/search")
async def search_components(
    q: str = Query(..., description="Search query"),
    component_type: Optional[str] = Query(None, description="Filter by type: CPU, GPU, RAM, MB, PSU, Storage"),
    max_price: Optional[float] = Query(None),
    brand: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):
    """
    Search PC components with Algolia
    Returns matching components with scores
    """
    filters = {}
    if component_type:
        filters["type"] = component_type
    if brand:
        filters["brand"] = brand
    if max_price:
        filters["price"] = f"0:{max_price}"  # Numeric range filter
    
    results = algolia_service.search_components(q, filters=filters, limit=limit)
    
    return {
        "query": q,
        "count": len(results),
        "results": results,
        "filters_applied": filters
    }

@router.get("/type/{component_type}")
async def get_by_type(
    component_type: str,
    brand: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    limit: int = Query(50)
):
    """
    Get all components of a specific type with optional filters
    """
    filters = {}
    if brand:
        filters["brand"] = brand
    if max_price:
        filters["price"] = f"0:{max_price}"
    
    results = algolia_service.search_by_type(component_type, filters=filters)
    return {
        "type": component_type,
        "count": len(results[:limit]),
        "results": results[:limit]
    }

@router.get("/facets")
async def get_facets(component_type: Optional[str] = Query(None)):
    """
    Get available filter options (brands, tiers, etc.)
    Useful for populating filter dropdowns in UI
    """
    facets = algolia_service.get_facets(component_type)
    return {
        "available_filters": facets
    }

@router.get("/{component_id}")
async def get_component_details(component_id: str):
    """Get detailed info about a specific component"""
    results = algolia_service.search_components(f"id:{component_id}")
    if results:
        return results[0]
    return {"error": "Component not found"}
```

### 3.4 Create Compatibility Checking Endpoints

**Compatibility Checker Service**
```python
# backend/app/services/compatibility_service.py
from typing import Dict, List, Tuple
from app.services.algolia_service import algolia_service

class CompatibilityService:
    
    @staticmethod
    def check_cpu_motherboard(cpu: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """Check if CPU socket matches motherboard socket"""
        cpu_socket = cpu.get("specs", {}).get("socket")
        mb_socket = motherboard.get("specs", {}).get("socket")
        
        if cpu_socket == mb_socket:
            return True, f"Compatible: Both use {cpu_socket}"
        return False, f"Incompatible: CPU {cpu_socket} vs MB {mb_socket}"
    
    @staticmethod
    def check_ram_motherboard(ram: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """Check if RAM type matches motherboard"""
        ram_type = ram.get("specs", {}).get("type")
        mb_memory_type = motherboard.get("specs", {}).get("memory_type")
        
        if ram_type == mb_memory_type:
            return True, f"Compatible: Both use {ram_type}"
        return False, f"Incompatible: RAM {ram_type} vs MB {mb_memory_type}"
    
    @staticmethod
    def check_gpu_motherboard(gpu: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """Check if motherboard has PCIe slot for GPU"""
        mb_pcie = motherboard.get("specs", {}).get("pcie_version", "3.0")
        gpu_pcie = gpu.get("specs", {}).get("pcie_version", "3.0")
        
        if float(mb_pcie) >= float(gpu_pcie):
            return True, f"Compatible: MB has PCIe {mb_pcie}"
        return False, f"Limited: MB is PCIe {mb_pcie}, GPU is {gpu_pcie}"
    
    @staticmethod
    def check_gpu_psu(gpu: Dict, psu: Dict) -> Tuple[bool, str]:
        """Check if PSU has enough wattage and connectors"""
        gpu_power = gpu.get("specs", {}).get("tdp", 200)
        psu_wattage = psu.get("specs", {}).get("wattage", 650)
        
        # Rule: PSU should be 1.25x total system power
        # Estimate system power = GPU TDP + 200W (CPU + other)
        estimated_total = gpu_power + 200
        required_psu = int(estimated_total * 1.25)
        
        if psu_wattage >= required_psu:
            return True, f"Compatible: {psu_wattage}W PSU sufficient for {gpu_power}W GPU"
        return False, f"Insufficient: Need {required_psu}W PSU, have {psu_wattage}W"
    
    @staticmethod
    def check_cpu_psu(cpu: Dict, psu: Dict) -> Tuple[bool, str]:
        """Check if PSU can power CPU"""
        cpu_tdp = cpu.get("specs", {}).get("tdp", 125)
        psu_wattage = psu.get("specs", {}).get("wattage", 650)
        
        if psu_wattage >= cpu_tdp * 2:  # PSU should handle 2x CPU power
            return True, f"Compatible: PSU adequate"
        return False, f"Possible issue: CPU TDP {cpu_tdp}W vs PSU {psu_wattage}W"
    
    @staticmethod
    def check_full_build(build: Dict) -> Dict:
        """
        Check all components in a build for compatibility
        build: Dict with keys like 'cpu', 'gpu', 'motherboard', 'ram', 'psu'
        """
        results = {
            "compatible": True,
            "checks": [],
            "warnings": [],
            "total_power": 0
        }
        
        cpu = build.get("cpu")
        motherboard = build.get("motherboard")
        gpu = build.get("gpu")
        psu = build.get("psu")
        ram = build.get("ram")
        
        # CPU-Motherboard
        if cpu and motherboard:
            compatible, msg = CompatibilityService.check_cpu_motherboard(cpu, motherboard)
            results["checks"].append({"check": "CPU-Motherboard", "compatible": compatible, "message": msg})
            if not compatible:
                results["compatible"] = False
        
        # RAM-Motherboard
        if ram and motherboard:
            compatible, msg = CompatibilityService.check_ram_motherboard(ram, motherboard)
            results["checks"].append({"check": "RAM-Motherboard", "compatible": compatible, "message": msg})
            if not compatible:
                results["compatible"] = False
        
        # GPU-Motherboard
        if gpu and motherboard:
            compatible, msg = CompatibilityService.check_gpu_motherboard(gpu, motherboard)
            results["checks"].append({"check": "GPU-Motherboard", "compatible": compatible, "message": msg})
            if not compatible:
                results["warnings"].append(msg)
        
        # GPU-PSU
        if gpu and psu:
            compatible, msg = CompatibilityService.check_gpu_psu(gpu, psu)
            results["checks"].append({"check": "GPU-PSU", "compatible": compatible, "message": msg})
            if not compatible:
                results["compatible"] = False
        
        # CPU-PSU
        if cpu and psu:
            compatible, msg = CompatibilityService.check_cpu_psu(cpu, psu)
            results["checks"].append({"check": "CPU-PSU", "compatible": compatible, "message": msg})
        
        # Calculate total power
        results["total_power"] = (cpu.get("specs", {}).get("tdp", 0) + 
                                 gpu.get("specs", {}).get("tdp", 0) + 150)
        
        return results

compatibility_service = CompatibilityService()
```

**Compatibility Endpoints**
```python
# backend/app/routes/compatibility.py
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.services.compatibility_service import compatibility_service
from app.services.algolia_service import algolia_service

router = APIRouter()

@router.post("/check-build")
async def check_build_compatibility(build: Dict):
    """
    Check compatibility of a complete PC build
    build: Dict with component IDs like {"cpu_id": "cpu_001", "gpu_id": "gpu_001", ...}
    """
    # Fetch actual component data from Algolia
    build_data = {}
    
    for component_type, component_id in build.items():
        if component_id:
            results = algolia_service.search_components(f"id:{component_id}")
            if results:
                build_data[component_type.replace("_id", "")] = results[0]
    
    result = compatibility_service.check_full_build(build_data)
    return result

@router.get("/check-pair/{component1_id}/{component2_id}")
async def check_component_pair(component1_id: str, component2_id: str):
    """Check compatibility between two components"""
    results1 = algolia_service.search_components(f"id:{component1_id}")
    results2 = algolia_service.search_components(f"id:{component2_id}")
    
    if not results1 or not results2:
        raise HTTPException(status_code=404, detail="Component not found")
    
    comp1, comp2 = results1[0], results2[0]
    
    # Determine component types and check accordingly
    type1, type2 = comp1.get("type"), comp2.get("type")
    
    if (type1 == "CPU" and type2 == "Motherboard") or (type1 == "Motherboard" and type2 == "CPU"):
        compatible, msg = compatibility_service.check_cpu_motherboard(comp1, comp2)
    elif (type1 == "RAM" and type2 == "Motherboard") or (type1 == "Motherboard" and type2 == "RAM"):
        compatible, msg = compatibility_service.check_ram_motherboard(comp1, comp2)
    else:
        return {"message": "Cannot check compatibility between these types"}
    
    return {"compatible": compatible, "message": msg}
```

### 3.5 Create Smart Suggestion Endpoints

**Suggestion Service**
```python
# backend/app/services/suggestion_service.py
from app.services.algolia_service import algolia_service
from typing import List, Dict

class SuggestionService:
    
    @staticmethod
    def suggest_cpus(budget: float = None, use_case: str = None) -> List[Dict]:
        """Suggest CPUs based on budget and use case"""
        filters = {}
        if use_case:
            filters["segment"] = use_case  # gaming, streaming, workstation
        
        query = "Intel AMD Ryzen"
        results = algolia_service.search_components(query, filters=filters, limit=10)
        
        if budget:
            results = [r for r in results if r.get("price", 0) <= budget]
        
        return sorted(results, key=lambda x: x.get("performance_tier", "budget"))
    
    @staticmethod
    def suggest_compatible_gpu(cpu: Dict, budget: float = None) -> List[Dict]:
        """
        Suggest GPUs that pair well with given CPU
        Avoid bottlenecking by matching performance tiers
        """
        cpu_tier = cpu.get("specs", {}).get("performance_tier", "mid-range")
        
        filters = {"performance_tier": cpu_tier}
        results = algolia_service.search_by_type("GPU", filters=filters)
        
        if budget:
            results = [r for r in results if r.get("price", 0) <= budget]
        
        return results[:5]
    
    @staticmethod
    def suggest_compatible_motherboard(cpu: Dict) -> List[Dict]:
        """Suggest motherboards compatible with CPU"""
        cpu_socket = cpu.get("specs", {}).get("socket")
        filters = {"socket": cpu_socket}
        
        return algolia_service.search_by_type("Motherboard", filters=filters)[:5]
    
    @staticmethod
    def suggest_ram(motherboard: Dict, budget: float = None) -> List[Dict]:
        """Suggest RAM compatible with motherboard"""
        memory_type = motherboard.get("specs", {}).get("memory_type", "DDR5")
        filters = {"type": memory_type}
        
        results = algolia_service.search_by_type("RAM", filters=filters)
        
        if budget:
            results = [r for r in results if r.get("price", 0) <= budget]
        
        return results[:5]
    
    @staticmethod
    def suggest_psu(total_power: int) -> List[Dict]:
        """Suggest PSU with 1.25x headroom"""
        recommended_wattage = int(total_power * 1.25)
        
        # Search for PSUs near recommended wattage
        results = algolia_service.search_by_type("PSU")
        
        # Filter by wattage
        suitable_psus = [r for r in results if r.get("specs", {}).get("wattage", 0) >= recommended_wattage]
        
        return sorted(suitable_psus, key=lambda x: x.get("price", 0))[:5]

suggestion_service = SuggestionService()
```

**Suggestion Endpoints**
```python
# backend/app/routes/suggestions.py
from fastapi import APIRouter, Query
from typing import Optional
from app.services.suggestion_service import suggestion_service
from app.services.algolia_service import algolia_service

router = APIRouter()

@router.get("/cpus")
async def suggest_cpus(
    budget: Optional[float] = Query(None),
    use_case: Optional[str] = Query(None, description="gaming, streaming, workstation, etc")
):
    """Get CPU suggestions based on budget and use case"""
    suggestions = suggestion_service.suggest_cpus(budget=budget, use_case=use_case)
    return {"suggestions": suggestions, "count": len(suggestions)}

@router.get("/compatible-gpu/{cpu_id}")
async def suggest_compatible_gpu(
    cpu_id: str,
    budget: Optional[float] = Query(None)
):
    """Suggest GPUs compatible with selected CPU"""
    results = algolia_service.search_components(f"id:{cpu_id}")
    if not results:
        return {"error": "CPU not found"}
    
    cpu = results[0]
    suggestions = suggestion_service.suggest_compatible_gpu(cpu, budget=budget)
    
    return {
        "for_cpu": cpu["name"],
        "suggestions": suggestions,
        "count": len(suggestions)
    }

@router.get("/compatible-motherboard/{cpu_id}")
async def suggest_compatible_motherboard(cpu_id: str):
    """Suggest compatible motherboards"""
    results = algolia_service.search_components(f"id:{cpu_id}")
    if not results:
        return {"error": "CPU not found"}
    
    cpu = results[0]
    suggestions = suggestion_service.suggest_compatible_motherboard(cpu)
    
    return {
        "for_cpu": cpu["name"],
        "suggestions": suggestions,
        "count": len(suggestions)
    }

@router.get("/ram/{motherboard_id}")
async def suggest_ram(
    motherboard_id: str,
    budget: Optional[float] = Query(None)
):
    """Suggest RAM compatible with motherboard"""
    results = algolia_service.search_components(f"id:{motherboard_id}")
    if not results:
        return {"error": "Motherboard not found"}
    
    motherboard = results[0]
    suggestions = suggestion_service.suggest_ram(motherboard, budget=budget)
    
    return {
        "for_motherboard": motherboard["name"],
        "suggestions": suggestions,
        "count": len(suggestions)
    }

@router.get("/psu")
async def suggest_psu(total_power: int = Query(..., description="Total system power in watts")):
    """Suggest PSU based on system power"""
    suggestions = suggestion_service.suggest_psu(total_power)
    
    return {
        "recommended_wattage": int(total_power * 1.25),
        "suggestions": suggestions,
        "count": len(suggestions)
    }
```

### 3.6 Error Handling & Logging

**Add Global Error Handler**
```python
# backend/app/utils/error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Add to main.py:
# app.add_exception_handler(Exception, global_exception_handler)
```

**Add Logging Throughout**
```python
# Add to services
import logging

logger = logging.getLogger(__name__)

# In methods:
logger.info(f"Searching for components: {query}")
logger.error(f"Algolia API error: {error}")
```

### 3.7 Testing Backend Endpoints

**Create Test File**
```python
# backend/tests/test_components.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_components():
    response = client.get("/api/components/search?q=Intel+i9")
    assert response.status_code == 200
    assert "results" in response.json()

def test_get_by_type():
    response = client.get("/api/components/type/CPU")
    assert response.status_code == 200
    assert "results" in response.json()

def test_compatibility_check():
    response = client.post("/api/compatibility/check-build", json={
        "cpu_id": "cpu_001",
        "motherboard_id": "mb_001"
    })
    assert response.status_code == 200
    assert "checks" in response.json()
```

### 3.8 Deployment Preparation

- [ ] Add `.env.example` with dummy values
- [ ] Create `requirements.txt`: `pip freeze > requirements.txt`
- [ ] Create `Dockerfile` for containerization
- [ ] Set up for Railway or Heroku deployment
- [ ] Configure production database connection
- [ ] Run API tests locally before deployment

## Phase 4: Frontend Development (Days 8-10)

### 4.1 React Project Structure & Setup

**Create Component Folder Structure**
```
frontend/src/
├── components/
│   ├── SearchBar.jsx           # Search & filter components
│   ├── ComponentCard.jsx        # Individual component display
│   ├── ComponentGrid.jsx        # Grid of components
│   ├── CompatibilityIndicator.jsx  # Shows compatibility status
│   ├── SuggestionPanel.jsx      # Shows smart suggestions
│   ├── BuildSummary.jsx         # Shows current build
│   └── FilterSidebar.jsx        # Filter options (brand, price, etc)
├── pages/
│   ├── HomePage.jsx            # Landing/intro
│   ├── BuilderPage.jsx         # Main builder interface
│   └── BuildSummaryPage.jsx    # Final build review
├── services/
│   ├── api.js                  # API calls to backend
│   ├── algolia.js              # Direct Algolia queries (optional)
│   └── storage.js              # Local storage for build
├── hooks/
│   ├── useBuild.js             # Build state management
│   ├── useSearch.js            # Search state management
│   └── useCompatibility.js     # Compatibility checking
├── styles/
│   ├── App.css                 # Global styles
│   └── components.css          # Component-specific styles
├── App.jsx
└── index.jsx
```

### 4.2 API Service Layer

**Create API Service**
```javascript
// frontend/src/services/api.js
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const apiClient = {
  // Component endpoints
  searchComponents: async (query, filters = {}, limit = 20) => {
    const params = new URLSearchParams({
      q: query,
      limit,
      ...filters
    });
    const response = await fetch(`${API_BASE}/components/search?${params}`);
    return response.json();
  },

  getComponentsByType: async (type, filters = {}) => {
    const params = new URLSearchParams({
      ...filters
    });
    const response = await fetch(`${API_BASE}/components/type/${type}?${params}`);
    return response.json();
  },

  getComponentDetails: async (componentId) => {
    const response = await fetch(`${API_BASE}/components/${componentId}`);
    return response.json();
  },

  getAvailableFilters: async (type) => {
    const response = await fetch(
      `${API_BASE}/components/facets${type ? `?component_type=${type}` : ''}`
    );
    return response.json();
  },

  // Compatibility endpoints
  checkBuildCompatibility: async (build) => {
    const response = await fetch(`${API_BASE}/compatibility/check-build`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(build)
    });
    return response.json();
  },

  checkComponentPair: async (id1, id2) => {
    const response = await fetch(`${API_BASE}/compatibility/check-pair/${id1}/${id2}`);
    return response.json();
  },

  // Suggestion endpoints
  suggestCPUs: async (budget, useCase) => {
    const params = new URLSearchParams();
    if (budget) params.append('budget', budget);
    if (useCase) params.append('use_case', useCase);
    const response = await fetch(`${API_BASE}/suggestions/cpus?${params}`);
    return response.json();
  },

  suggestCompatibleGPU: async (cpuId, budget) => {
    const params = new URLSearchParams();
    if (budget) params.append('budget', budget);
    const response = await fetch(`${API_BASE}/suggestions/compatible-gpu/${cpuId}?${params}`);
    return response.json();
  },

  suggestCompatibleMotherboard: async (cpuId) => {
    const response = await fetch(`${API_BASE}/suggestions/compatible-motherboard/${cpuId}`);
    return response.json();
  },

  suggestRAM: async (motherboardId, budget) => {
    const params = new URLSearchParams();
    if (budget) params.append('budget', budget);
    const response = await fetch(`${API_BASE}/suggestions/ram/${motherboardId}?${params}`);
    return response.json();
  },

  suggestPSU: async (totalPower) => {
    const response = await fetch(`${API_BASE}/suggestions/psu?total_power=${totalPower}`);
    return response.json();
  }
};
```

### 4.3 Custom Hooks for State Management

**Build Management Hook**
```javascript
// frontend/src/hooks/useBuild.js
import { useState, useEffect } from 'react';

export const useBuild = () => {
  const [build, setBuild] = useState({
    cpu: null,
    motherboard: null,
    gpu: null,
    ram: null,
    psu: null,
    storage: []
  });

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('pcBuild');
    if (saved) {
      setBuild(JSON.parse(saved));
    }
  }, []);

  // Save to localStorage when build changes
  useEffect(() => {
    localStorage.setItem('pcBuild', JSON.stringify(build));
  }, [build]);

  const addComponent = (type, component) => {
    if (type === 'storage') {
      setBuild(prev => ({
        ...prev,
        storage: [...prev.storage, component]
      }));
    } else {
      setBuild(prev => ({
        ...prev,
        [type]: component
      }));
    }
  };

  const removeComponent = (type, index = 0) => {
    if (type === 'storage') {
      setBuild(prev => ({
        ...prev,
        storage: prev.storage.filter((_, i) => i !== index)
      }));
    } else {
      setBuild(prev => ({
        ...prev,
        [type]: null
      }));
    }
  };

  const calculateTotalPrice = () => {
    let total = 0;
    Object.values(build).forEach(component => {
      if (Array.isArray(component)) {
        total += component.reduce((sum, c) => sum + (c.price || 0), 0);
      } else if (component) {
        total += component.price || 0;
      }
    });
    return total;
  };

  const calculateTotalPower = () => {
    let power = 0;
    if (build.cpu) power += build.cpu.specs?.tdp || 0;
    if (build.gpu) power += build.gpu.specs?.tdp || 0;
    power += 150; // System overhead
    return power;
  };

  return {
    build,
    addComponent,
    removeComponent,
    calculateTotalPrice,
    calculateTotalPower
  };
};
```

**Search Hook**
```javascript
// frontend/src/hooks/useSearch.js
import { useState } from 'react';
import { apiClient } from '../services/api';

export const useSearch = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async (query, filters = {}) => {
    setLoading(true);
    try {
      const data = await apiClient.searchComponents(query, filters);
      setResults(data.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const searchByType = async (type, filters = {}) => {
    setLoading(true);
    try {
      const data = await apiClient.getComponentsByType(type, filters);
      setResults(data.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { results, loading, error, search, searchByType };
};
```

**Compatibility Hook**
```javascript
// frontend/src/hooks/useCompatibility.js
import { useState } from 'react';
import { apiClient } from '../services/api';

export const useCompatibility = () => {
  const [compatibility, setCompatibility] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkBuild = async (build) => {
    setLoading(true);
    try {
      const data = await apiClient.checkBuildCompatibility(build);
      setCompatibility(data);
    } catch (err) {
      console.error('Compatibility check failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return { compatibility, loading, checkBuild };
};
```

### 4.4 Build Core Components

**ComponentCard.jsx - Display individual component**
```javascript
// frontend/src/components/ComponentCard.jsx
import React from 'react';
import './ComponentCard.css';

export const ComponentCard = ({ component, onSelect, isSelected }) => {
  return (
    <div className={`component-card ${isSelected ? 'selected' : ''}`}>
      <div className="card-header">
        <h3>{component.name}</h3>
        <span className="brand">{component.brand}</span>
      </div>
      
      <div className="card-specs">
        {component.specs && Object.entries(component.specs).map(([key, value]) => (
          <div key={key} className="spec-item">
            <span className="spec-key">{key}:</span>
            <span className="spec-value">{JSON.stringify(value)}</span>
          </div>
        ))}
      </div>
      
      <div className="card-footer">
        <span className="price">${component.price?.toFixed(2)}</span>
        <button 
          onClick={() => onSelect(component)}
          className={isSelected ? 'btn-selected' : 'btn-select'}
        >
          {isSelected ? '✓ Selected' : 'Select'}
        </button>
      </div>
    </div>
  );
};
```

**SearchBar.jsx - Search & filter interface**
```javascript
// frontend/src/components/SearchBar.jsx
import React, { useState } from 'react';

export const SearchBar = ({ onSearch, onFilterChange }) => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({});

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(query, filters);
  };

  const handleFilterChange = (filterType, value) => {
    const newFilters = { ...filters, [filterType]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search components..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      
      <div className="filters">
        <select onChange={(e) => handleFilterChange('component_type', e.target.value)}>
          <option value="">All Types</option>
          <option value="CPU">CPU</option>
          <option value="GPU">GPU</option>
          <option value="RAM">RAM</option>
          <option value="Motherboard">Motherboard</option>
          <option value="PSU">PSU</option>
          <option value="Storage">Storage</option>
        </select>

        <input
          type="number"
          placeholder="Max Price"
          onChange={(e) => handleFilterChange('max_price', e.target.value)}
        />
      </div>
    </div>
  );
};
```

**SuggestionPanel.jsx - Show smart suggestions**
```javascript
// frontend/src/components/SuggestionPanel.jsx
import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';
import { ComponentCard } from './ComponentCard';

export const SuggestionPanel = ({ selectedComponent, componentType, onComponentSelect }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!selectedComponent || !selectedComponent.id) return;

    setLoading(true);
    
    const fetchSuggestions = async () => {
      try {
        let data;
        if (componentType === 'CPU') {
          data = await apiClient.suggestCompatibleMotherboard(selectedComponent.id);
        } else if (componentType === 'Motherboard') {
          data = await apiClient.suggestRAM(selectedComponent.id);
        } else if (componentType === 'GPU') {
          // Could suggest compatible CPU
          data = { suggestions: [] };
        }
        setSuggestions(data.suggestions || []);
      } catch (err) {
        console.error('Failed to fetch suggestions:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [selectedComponent, componentType]);

  if (loading) return <div>Loading suggestions...</div>;

  return (
    <div className="suggestion-panel">
      <h3>Compatible Components</h3>
      <div className="suggestion-grid">
        {suggestions.map(component => (
          <ComponentCard
            key={component.id}
            component={component}
            onSelect={() => onComponentSelect(component)}
          />
        ))}
      </div>
    </div>
  );
};
```

**CompatibilityIndicator.jsx**
```javascript
// frontend/src/components/CompatibilityIndicator.jsx
import React from 'react';
import './CompatibilityIndicator.css';

export const CompatibilityIndicator = ({ checks, compatible }) => {
  return (
    <div className={`compatibility-indicator ${compatible ? 'compatible' : 'incompatible'}`}>
      <h3>Compatibility Check</h3>
      {compatible ? (
        <div className="compatible-badge">✓ All components compatible</div>
      ) : (
        <div className="incompatible-badge">✗ Compatibility issues found</div>
      )}
      
      <div className="checks-list">
        {checks?.map((check, idx) => (
          <div key={idx} className={`check-item ${check.compatible ? 'pass' : 'fail'}`}>
            <span className="check-icon">
              {check.compatible ? '✓' : '✗'}
            </span>
            <span className="check-name">{check.check}</span>
            <span className="check-message">{check.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 4.5 Build Main BuilderPage

**BuilderPage.jsx - Main interface**
```javascript
// frontend/src/pages/BuilderPage.jsx
import React, { useState } from 'react';
import { SearchBar } from '../components/SearchBar';
import { ComponentCard } from '../components/ComponentCard';
import { SuggestionPanel } from '../components/SuggestionPanel';
import { CompatibilityIndicator } from '../components/CompatibilityIndicator';
import { useBuild } from '../hooks/useBuild';
import { useSearch } from '../hooks/useSearch';
import { useCompatibility } from '../hooks/useCompatibility';
import { apiClient } from '../services/api';

export const BuilderPage = () => {
  const { build, addComponent, calculateTotalPrice, calculateTotalPower } = useBuild();
  const { results, loading, search, searchByType } = useSearch();
  const { compatibility, checkBuild } = useCompatibility();
  const [activeTab, setActiveTab] = useState('cpu');

  const handleComponentSelect = (component) => {
    addComponent(activeTab, component);
    
    // Check compatibility after each selection
    const updatedBuild = {
      ...build,
      [activeTab]: component
    };
    checkBuild(updatedBuild);
  };

  const handleSearch = (query, filters) => {
    if (query) {
      search(query, filters);
    } else {
      searchByType(activeTab, filters);
    }
  };

  return (
    <div className="builder-page">
      <div className="builder-container">
        
        {/* Left: Search & Results */}
        <div className="search-section">
          <SearchBar onSearch={handleSearch} onFilterChange={() => {}} />
          
          <div className="tabs">
            {['cpu', 'motherboard', 'gpu', 'ram', 'psu', 'storage'].map(tab => (
              <button
                key={tab}
                className={`tab ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab.toUpperCase()}
              </button>
            ))}
          </div>

          <div className="results">
            {loading && <p>Loading...</p>}
            {results.map(component => (
              <ComponentCard
                key={component.id}
                component={component}
                onSelect={handleComponentSelect}
                isSelected={build[activeTab]?.id === component.id}
              />
            ))}
          </div>
        </div>

        {/* Right: Build Summary & Suggestions */}
        <div className="summary-section">
          <div className="build-summary">
            <h2>Your Build</h2>
            {Object.entries(build).map(([type, component]) => (
              component && (
                <div key={type} className="selected-component">
                  <strong>{type}:</strong> {component.name} - ${component.price}
                </div>
              )
            ))}
            
            <div className="build-stats">
              <div>Total: ${calculateTotalPrice().toFixed(2)}</div>
              <div>Power: {calculateTotalPower()}W</div>
            </div>
          </div>

          {compatibility && (
            <CompatibilityIndicator
              checks={compatibility.checks}
              compatible={compatibility.compatible}
            />
          )}

          {build[activeTab] && (
            <SuggestionPanel
              selectedComponent={build[activeTab]}
              componentType={activeTab}
              onComponentSelect={handleComponentSelect}
            />
          )}
        </div>
      </div>
    </div>
  );
};
```

### 4.6 Styling with Tailwind/CSS

**BuilderPage.css - Main styling**
```css
.builder-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.search-section, .summary-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.tab.active {
  background: #007bff;
  color: white;
  border-color: #0056b3;
}

.results {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  max-height: 600px;
  overflow-y: auto;
}

.component-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.component-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.component-card.selected {
  border-color: #28a745;
  background: #f0f8f5;
}

.build-summary {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
}

.selected-component {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.build-stats {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #ddd;
  font-weight: bold;
}

@media (max-width: 768px) {
  .builder-page {
    grid-template-columns: 1fr;
  }
}
```

### 4.7 Create Additional Pages

**HomePage.jsx - Landing page**
```javascript
// frontend/src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export const HomePage = () => {
  return (
    <div className="home-page">
      <h1>PCBuild Assist</h1>
      <p>Build your perfect PC with intelligent component compatibility checking</p>
      <Link to="/builder" className="btn-primary">Start Building</Link>
    </div>
  );
};
```

### 4.8 App.jsx Setup with Routing

```javascript
// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { BuilderPage } from './pages/BuilderPage';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/builder" element={<BuilderPage />} />
      </Routes>
    </Router>
  );
}

export default App;
```

## Phase 5: Integration & Intelligence (Days 11-12)

### 5.1 Connect Frontend to Backend API

**Environment Configuration**
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ALGOLIA_APP_ID=your_algolia_app_id
REACT_APP_ALGOLIA_SEARCH_KEY=your_search_key
```

**API Interceptor for Error Handling**
```javascript
// frontend/src/services/api.js - Enhanced
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API Error');
  }
  return response.json();
};

const fetchWithErrorHandling = (url, options = {}) => {
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  }).then(handleResponse);
};

export const apiClient = {
  searchComponents: (query, filters = {}, limit = 20) =>
    fetchWithErrorHandling(
      `${API_BASE}/components/search?q=${query}&limit=${limit}&${new URLSearchParams(filters)}`
    ),

  // ... other methods with error handling
};
```

### 5.2 Integrate Algolia Agent Studio

**Setup Algolia Agent Studio Connection**
```javascript
// frontend/src/services/algolia-agent.js
import algoliasearch from 'algoliasearch';

const searchClient = algoliasearch(
  process.env.REACT_APP_ALGOLIA_APP_ID,
  process.env.REACT_APP_ALGOLIA_SEARCH_KEY
);

const index = searchClient.initIndex('pc_components');

export const algoliaAgent = {
  /**
   * Direct search using Algolia (optional, for advanced queries)
   */
  search: async (query, filters = {}) => {
    const searchParams = {
      query,
      hitsPerPage: 20,
      analytics: true,  // Track for insights
      clickAnalytics: true  // Track user interactions
    };

    if (filters.brand) {
      searchParams.facetFilters = [`brand:${filters.brand}`];
    }

    const response = await index.search(query, searchParams);
    return response;
  },

  /**
   * Get facets for filtering
   */
  getFacets: async (facetName) => {
    const response = await index.searchForFacetValues(facetName, '');
    return response.facetHits;
  },

  /**
   * Get recommendations based on current component
   */
  getRecommendations: async (componentId) => {
    // Would use Algolia's personalization/recommendation API
    // This is where you'd call backend suggestions endpoint
    return [];
  }
};
```

**Create Agent-Powered Suggestion Component**
```javascript
// frontend/src/components/AIAssistant.jsx
import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';
import { algoliaAgent } from '../services/algolia-agent';

export const AIAssistant = ({ build, onSuggestionSelect }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [insight, setInsight] = useState('');

  useEffect(() => {
    generateIntelligentSuggestions();
  }, [build]);

  const generateIntelligentSuggestions = async () => {
    // Analyze current build and generate smart suggestions
    
    if (!build.cpu && !build.motherboard) {
      // Suggest starting with CPU + Motherboard combo
      try {
        const cpuData = await apiClient.suggestCPUs(
          build.budget,
          build.useCase || 'gaming'
        );
        setSuggestions(cpuData.suggestions || []);
        setInsight('👉 Start by selecting a CPU - we\'ll suggest compatible components');
      } catch (err) {
        console.error('Failed to get suggestions:', err);
      }
    } else if (build.cpu && !build.motherboard) {
      // Suggest compatible motherboard
      try {
        const mbData = await apiClient.suggestCompatibleMotherboard(build.cpu.id);
        setSuggestions(mbData.suggestions || []);
        setInsight(`✓ CPU selected. Next: Choose a ${build.cpu.specs?.socket || 'compatible'} motherboard`);
      } catch (err) {
        console.error('Failed to get motherboard suggestions:', err);
      }
    } else if (build.motherboard && !build.ram) {
      // Suggest compatible RAM
      try {
        const ramData = await apiClient.suggestRAM(build.motherboard.id);
        setSuggestions(ramData.suggestions || []);
        setInsight('✓ Motherboard selected. Next: Choose compatible RAM');
      } catch (err) {
        console.error('Failed to get RAM suggestions:', err);
      }
    } else if (build.cpu && !build.gpu) {
      // Suggest balanced GPU
      try {
        const gpuData = await apiClient.suggestCompatibleGPU(
          build.cpu.id,
          build.budget
        );
        setSuggestions(gpuData.suggestions || []);
        setInsight('✓ CPU and RAM configured. Next: Choose a GPU to match your CPU tier');
      } catch (err) {
        console.error('Failed to get GPU suggestions:', err);
      }
    } else if (build.cpu && build.gpu && !build.psu) {
      // Suggest PSU based on total power
      const totalPower = (build.cpu.specs?.tdp || 0) + (build.gpu.specs?.tdp || 0) + 150;
      try {
        const psuData = await apiClient.suggestPSU(totalPower);
        setSuggestions(psuData.suggestions || []);
        setInsight(`✓ GPU selected. Next: Get a ${totalPower * 1.25}W+ PSU for your build`);
      } catch (err) {
        console.error('Failed to get PSU suggestions:', err);
      }
    }
  };

  return (
    <div className="ai-assistant">
      <div className="insight-box">
        <h3>💡 Assistant</h3>
        <p>{insight}</p>
      </div>
      
      <div className="suggestions">
        <h4>Recommended Components</h4>
        {suggestions.length > 0 ? (
          <div className="suggestion-items">
            {suggestions.slice(0, 3).map(item => (
              <div key={item.id} className="suggestion-item">
                <h5>{item.name}</h5>
                <p>${item.price}</p>
                <button onClick={() => onSuggestionSelect(item)}>
                  Add to Build →
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>No suggestions at this stage</p>
        )}
      </div>
    </div>
  );
};
```

### 5.3 Real-Time Search Integration

**Debounced Search Component**
```javascript
// frontend/src/hooks/useDebouncedSearch.js
import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '../services/api';

export const useDebouncedSearch = (delay = 300) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const timeoutRef = React.useRef(null);

  const search = useCallback((query, filters = {}) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    setLoading(true);
    timeoutRef.current = setTimeout(async () => {
      try {
        const data = await apiClient.searchComponents(query, filters);
        setResults(data.results || []);
      } catch (err) {
        console.error('Search failed:', err);
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, delay);
  }, [delay]);

  return { results, loading, search };
};
```

**Live Search Bar Component**
```javascript
// frontend/src/components/LiveSearchBar.jsx
import React, { useState } from 'react';
import { useDebouncedSearch } from '../hooks/useDebouncedSearch';

export const LiveSearchBar = ({ onComponentSelect, componentType }) => {
  const [query, setQuery] = useState('');
  const { results, loading, search } = useDebouncedSearch(300);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    
    if (value.length > 2) {
      search(value, { component_type: componentType });
    }
  };

  return (
    <div className="live-search">
      <input
        type="text"
        placeholder={`Search ${componentType}s...`}
        value={query}
        onChange={handleInputChange}
        className="search-input"
      />
      
      {loading && <span className="loading">Searching...</span>}
      
      {results.length > 0 && (
        <div className="search-dropdown">
          {results.slice(0, 5).map(result => (
            <div
              key={result.id}
              className="search-result"
              onClick={() => {
                onComponentSelect(result);
                setQuery('');
              }}
            >
              <strong>{result.name}</strong>
              <span className="price">${result.price}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### 5.4 Proactive Smart Suggestions Algorithm

**Intelligent Suggestion Logic**
```javascript
// frontend/src/services/suggestion-engine.js
export const suggestionEngine = {
  /**
   * Score components based on current build context
   */
  scoreComponent: (component, build, context) => {
    let score = 50; // Base score

    // Factor 1: Price compatibility
    if (build.budget) {
      if (component.price <= build.budget * 0.15) {
        score += 30; // Good price for tier
      } else if (component.price <= build.budget * 0.25) {
        score += 15;
      } else {
        score -= 20; // Over budget for this category
      }
    }

    // Factor 2: Performance tier match
    if (build.performanceTier) {
      if (component.specs?.performance_tier === build.performanceTier) {
        score += 25; // Perfect match
      } else if (context.suggestions?.includes(component.type)) {
        score += 10;
      }
    }

    // Factor 3: Recency (newer components preferred)
    if (component.specs?.release_year >= 2024) {
      score += 15;
    }

    // Factor 4: Popularity (if available)
    if (component.popularity) {
      score += Math.min(component.popularity * 10, 20);
    }

    return Math.min(score, 100);
  },

  /**
   * Generate build recommendations based on use case
   */
  recommendBuild: (useCase, budget) => {
    const templates = {
      gaming: {
        cpuTier: 'mid-range-high',
        gpuTier: 'mid-range-high',
        ramGB: 32,
        psuWatts: 750,
        storageGB: 1000
      },
      streaming: {
        cpuTier: 'high-end',
        gpuTier: 'high-end',
        ramGB: 64,
        psuWatts: 1000,
        storageGB: 2000
      },
      workstation: {
        cpuTier: 'high-end',
        gpuTier: 'professional',
        ramGB: 64,
        psuWatts: 850,
        storageGB: 2000
      },
      budget: {
        cpuTier: 'budget',
        gpuTier: 'budget',
        ramGB: 16,
        psuWatts: 550,
        storageGB: 500
      }
    };

    return templates[useCase] || templates.gaming;
  }
};
```

### 5.5 Backend Optimization

**Add Caching to Speed Up Queries**
```python
# backend/app/utils/cache.py
from functools import wraps
import time

cache_store = {}

def cache_result(ttl=300):
    """Cache decorator with TTL (Time To Live)"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            if cache_key in cache_store:
                result, timestamp = cache_store[cache_key]
                if time.time() - timestamp < ttl:
                    return result
            
            result = await func(*args, **kwargs)
            cache_store[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator

# Usage in services:
from app.utils.cache import cache_result

class AlgoliaService:
    @cache_result(ttl=600)  # Cache for 10 minutes
    async def search_components(self, query, filters):
        # ... search logic
        pass
```

**Add Pagination for Large Result Sets**
```python
# In components route
@router.get("/search")
async def search_components(
    q: str,
    limit: int = 20,
    offset: int = 0
):
    results = algolia_service.search_components(q, limit=limit+offset)
    
    return {
        "results": results[offset:offset+limit],
        "total": len(results),
        "offset": offset,
        "limit": limit,
        "hasMore": offset + limit < len(results)
    }
```

### 5.6 Performance Monitoring

**Add Logging & Metrics**
```python
# backend/app/utils/metrics.py
import time
import logging

logger = logging.getLogger(__name__)

class RequestMetrics:
    @staticmethod
    def log_request(endpoint, duration, result_count):
        logger.info(
            f"Endpoint: {endpoint} | Duration: {duration:.2f}ms | Results: {result_count}"
        )

# In routes:
@router.get("/search")
async def search_components(q: str, filters: dict = {}):
    start = time.time()
    results = algolia_service.search_components(q, filters)
    duration = (time.time() - start) * 1000
    
    RequestMetrics.log_request("/components/search", duration, len(results))
    
    return {"results": results}
```

### 5.7 Frontend Performance Optimization

**Code Splitting & Lazy Loading**
```javascript
// frontend/src/App.jsx
import React, { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';

const BuilderPage = lazy(() => import('./pages/BuilderPage'));
const BuildSummaryPage = lazy(() => import('./pages/BuildSummaryPage'));

export const Loading = () => <div>Loading...</div>;

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/builder"
          element={
            <Suspense fallback={<Loading />}>
              <BuilderPage />
            </Suspense>
          }
        />
        <Route
          path="/summary"
          element={
            <Suspense fallback={<Loading />}>
              <BuildSummaryPage />
            </Suspense>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
```

**Memoization & Optimization**
```javascript
// Avoid unnecessary re-renders
import React, { memo } from 'react';

export const ComponentCard = memo(({ component, onSelect }) => {
  return (
    <div className="component-card" onClick={() => onSelect(component)}>
      {/* Card content */}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.component.id === nextProps.component.id;
});
```

### 5.8 Integration Testing

**Test Frontend-Backend Integration**
```javascript
// frontend/src/__tests__/integration.test.js
import { apiClient } from '../services/api';

describe('Frontend-Backend Integration', () => {
  test('should search components from backend', async () => {
    const result = await apiClient.searchComponents('Intel i9');
    expect(result.results).toBeDefined();
    expect(result.results.length).toBeGreaterThan(0);
  });

  test('should check compatibility', async () => {
    const build = {
      cpu_id: 'cpu_001',
      motherboard_id: 'mb_001'
    };
    const result = await apiClient.checkBuildCompatibility(build);
    expect(result.checks).toBeDefined();
  });

  test('should get suggestions', async () => {
    const result = await apiClient.suggestCPUs(1500);
    expect(result.suggestions).toBeDefined();
  });
});
```

## Phase 6: Testing & Deployment (Days 13-14)

### 6.1 Unit Testing

**Backend Unit Tests**
```python
# backend/tests/test_compatibility.py
import pytest
from app.services.compatibility_service import CompatibilityService

class TestCompatibility:
    def test_cpu_motherboard_compatible(self):
        cpu = {"specs": {"socket": "LGA1700"}}
        mb = {"specs": {"socket": "LGA1700"}}
        compatible, msg = CompatibilityService.check_cpu_motherboard(cpu, mb)
        assert compatible == True
    
    def test_cpu_motherboard_incompatible(self):
        cpu = {"specs": {"socket": "LGA1700"}}
        mb = {"specs": {"socket": "AM5"}}
        compatible, msg = CompatibilityService.check_cpu_motherboard(cpu, mb)
        assert compatible == False
    
    def test_ram_motherboard_compatible(self):
        ram = {"specs": {"type": "DDR5"}}
        mb = {"specs": {"memory_type": "DDR5"}}
        compatible, msg = CompatibilityService.check_ram_motherboard(ram, mb)
        assert compatible == True
    
    def test_gpu_psu_wattage(self):
        gpu = {"specs": {"tdp": 450}}
        psu = {"specs": {"wattage": 1000}}
        compatible, msg = CompatibilityService.check_gpu_psu(gpu, psu)
        assert compatible == True
    
    def test_gpu_psu_insufficient_wattage(self):
        gpu = {"specs": {"tdp": 450}}
        psu = {"specs": {"wattage": 500}}
        compatible, msg = CompatibilityService.check_gpu_psu(gpu, psu)
        assert compatible == False

    def test_full_build_check(self):
        build = {
            "cpu": {"specs": {"socket": "LGA1700", "tdp": 125}},
            "motherboard": {"specs": {"socket": "LGA1700", "memory_type": "DDR5"}},
            "ram": {"specs": {"type": "DDR5"}},
            "gpu": {"specs": {"tdp": 200}},
            "psu": {"specs": {"wattage": 850}}
        }
        result = CompatibilityService.check_full_build(build)
        assert result["compatible"] == True
        assert len(result["checks"]) > 0
```

**Frontend Component Tests**
```javascript
// frontend/src/__tests__/components/ComponentCard.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentCard } from '../../components/ComponentCard';

describe('ComponentCard', () => {
  const mockComponent = {
    id: 'cpu_001',
    name: 'Intel Core i9-13900K',
    brand: 'Intel',
    price: 589.99,
    specs: {
      cores: 24,
      tdp: 253
    }
  };

  test('renders component name', () => {
    render(<ComponentCard component={mockComponent} onSelect={() => {}} />);
    expect(screen.getByText('Intel Core i9-13900K')).toBeInTheDocument();
  });

  test('renders price', () => {
    render(<ComponentCard component={mockComponent} onSelect={() => {}} />);
    expect(screen.getByText('$589.99')).toBeInTheDocument();
  });

  test('calls onSelect when button clicked', async () => {
    const mockOnSelect = jest.fn();
    render(<ComponentCard component={mockComponent} onSelect={mockOnSelect} />);
    
    const button = screen.getByText('Select');
    await userEvent.click(button);
    
    expect(mockOnSelect).toHaveBeenCalledWith(mockComponent);
  });

  test('shows selected state', () => {
    const { container } = render(
      <ComponentCard component={mockComponent} onSelect={() => {}} isSelected={true} />
    );
    expect(container.querySelector('.component-card.selected')).toBeInTheDocument();
  });
});
```

**API Route Tests**
```python
# backend/tests/test_routes.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestComponentRoutes:
    def test_search_endpoint(self):
        response = client.get("/api/components/search?q=Intel")
        assert response.status_code == 200
        assert "results" in response.json()
    
    def test_search_with_filters(self):
        response = client.get("/api/components/search?q=CPU&component_type=CPU&max_price=1000")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
    
    def test_get_by_type(self):
        response = client.get("/api/components/type/CPU")
        assert response.status_code == 200
        assert "results" in response.json()

class TestCompatibilityRoutes:
    def test_check_build_compatibility(self):
        build = {
            "cpu_id": "cpu_001",
            "motherboard_id": "mb_001",
            "gpu_id": "gpu_001",
            "psu_id": "psu_001"
        }
        response = client.post("/api/compatibility/check-build", json=build)
        assert response.status_code == 200
        data = response.json()
        assert "compatible" in data
        assert "checks" in data
```

### 6.2 Integration Testing

**End-to-End Test**
```python
# backend/tests/test_e2e.py
@pytest.mark.asyncio
async def test_complete_build_workflow():
    """Test complete workflow: search → select → check compatibility → get suggestions"""
    
    # 1. Search for CPU
    cpu_response = client.get("/api/components/search?q=Intel+i9")
    assert cpu_response.status_code == 200
    cpus = cpu_response.json()["results"]
    assert len(cpus) > 0
    selected_cpu = cpus[0]
    
    # 2. Suggest compatible motherboard
    mb_response = client.get(f"/api/suggestions/compatible-motherboard/{selected_cpu['id']}")
    assert mb_response.status_code == 200
    mbs = mb_response.json()["suggestions"]
    assert len(mbs) > 0
    selected_mb = mbs[0]
    
    # 3. Suggest compatible RAM
    ram_response = client.get(f"/api/suggestions/ram/{selected_mb['id']}")
    assert ram_response.status_code == 200
    rams = ram_response.json()["suggestions"]
    assert len(rams) > 0
    
    # 4. Check full build compatibility
    build_check = client.post("/api/compatibility/check-build", json={
        "cpu_id": selected_cpu["id"],
        "motherboard_id": selected_mb["id"]
    })
    assert build_check.status_code == 200
    result = build_check.json()
    assert result["compatible"] == True
```

### 6.3 Load Testing

**Load Test with Locust**
```python
# load_test.py
from locust import HttpUser, task, between

class PCBuildAssistUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def search_components(self):
        self.client.get("/api/components/search?q=Intel&limit=20")
    
    @task(2)
    def get_by_type(self):
        self.client.get("/api/components/type/CPU")
    
    @task(1)
    def check_compatibility(self):
        self.client.post("/api/compatibility/check-build", json={
            "cpu_id": "cpu_001",
            "motherboard_id": "mb_001"
        })

# Run with: locust -f load_test.py --host=http://localhost:5000
```

**Run Load Test:**
```bash
locust -f load_test.py --host=http://localhost:5000 -u 100 -r 10 --run-time 5m
```

### 6.4 Frontend Manual Testing Checklist

- [ ] Search functionality works with various queries
- [ ] Filters (brand, price, type) work correctly
- [ ] Component selection updates build summary
- [ ] Compatibility indicators show correct status
- [ ] Smart suggestions appear contextually
- [ ] Build summary displays total price and power
- [ ] Local storage saves build between sessions
- [ ] Responsive design works on mobile/tablet
- [ ] Error messages display appropriately
- [ ] Loading states show during API calls

### 6.5 Deployment to Production

**Deploy Backend to Railway or Heroku**

**Option A: Railway (Recommended)**
```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set ALGOLIA_APP_ID=your_id
railway variables set ALGOLIA_ADMIN_API_KEY=your_key
railway variables set DATABASE_URL=your_db_url

# 5. Deploy
railway up

# Get URL
railway status
```

**Option B: Heroku**
```bash
# 1. Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Create app
heroku create pcbuild-assist-api

# 4. Set config vars
heroku config:set ALGOLIA_APP_ID=your_id
heroku config:set ALGOLIA_ADMIN_API_KEY=your_key

# 5. Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Deploy Frontend to Vercel or Netlify**

**Option A: Vercel (Recommended for React)**
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Set environment variables in Vercel dashboard
# REACT_APP_API_URL = https://your-backend.railway.app/api

# 4. Future deployments
vercel --prod
```

**Option B: Netlify**
```bash
# 1. Build frontend
npm run build

# 2. Install Netlify CLI
npm i -g netlify-cli

# 3. Deploy
netlify deploy --prod --dir=build
```

**Dockerfile for Backend**
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY .env .

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

**Docker Compose for Full Stack**
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - ALGOLIA_APP_ID=${ALGOLIA_APP_ID}
      - ALGOLIA_ADMIN_API_KEY=${ALGOLIA_ADMIN_API_KEY}
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:5000/api

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=pc_builder
    ports:
      - "5432:5432"
```

### 6.6 Setup CI/CD Pipeline

**GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt pytest
          pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### 6.7 Pre-Production Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Algolia index populated
- [ ] SSL/HTTPS enabled
- [ ] CORS configured for production
- [ ] Rate limiting enabled
- [ ] Health checks configured
- [ ] Database backups automated

### 6.8 Post-Deployment Verification

```bash
# Check backend health
curl https://your-backend.railway.app/health

# Check API
curl https://your-backend.railway.app/api/components/facets

# Test search
curl "https://your-backend.railway.app/api/components/search?q=Intel"
```

## Phase 7: Documentation & Submission (Day 15)

### 7.1 Create Comprehensive README

**README.md Structure**
```markdown
# PCBuild Assist - Algolia Challenge Submission

## Overview
A smart PC component builder that uses Algolia Agent Studio to proactively suggest compatible PC components without requiring conversational interaction. The app demonstrates real-time compatibility checking and contextual AI-powered recommendations.

## Key Features
- **Component Search**: Fast search across CPU, GPU, RAM, Motherboard, PSU, and Storage
- **Real-time Compatibility Checking**: Instant validation of component compatibility
- **Proactive Suggestions**: Smart suggestions appear contextually as you build
- **Performance Analysis**: Calculate total system power and price
- **Persistent Build**: Save your build to local storage for later

## Technology Stack
- **Frontend**: React + Vite
- **Backend**: Python FastAPI
- **Search**: Algolia (with Agent Studio)
- **Database**: PostgreSQL
- **Deployment**: Vercel (frontend), Railway (backend)

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- Algolia Account (Free Plan)
- PostgreSQL (optional for production)

### Local Development

#### 1. Clone Repository
\`\`\`bash
git clone https://github.com/yourusername/pcbuild_assist.git
cd pcbuild_assist
\`\`\`

#### 2. Backend Setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Algolia credentials

# Start backend
uvicorn app.main:app --reload
\`\`\`

#### 3. Frontend Setup
\`\`\`bash
cd frontend
npm install

# Create .env.local
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env.local

# Start frontend
npm run dev
\`\`\`

Visit `http://localhost:3000` to see the app.

## API Documentation

### Search Endpoints
- `GET /api/components/search?q=Intel&limit=20` - Search components
- `GET /api/components/type/{type}` - Get components by type
- `GET /api/components/facets` - Get available filters

### Compatibility Endpoints
- `POST /api/compatibility/check-build` - Check full build compatibility
- `GET /api/compatibility/check-pair/{id1}/{id2}` - Check two components

### Suggestion Endpoints
- `GET /api/suggestions/cpus?budget=1500&use_case=gaming`
- `GET /api/suggestions/compatible-gpu/{cpu_id}`
- `GET /api/suggestions/compatible-motherboard/{cpu_id}`
- `GET /api/suggestions/ram/{motherboard_id}`
- `GET /api/suggestions/psu?total_power=600`

## How Algolia Integration Demonstrates Non-Conversational Intelligence

1. **Search**: User types component name → Algolia instantly returns relevant results
2. **Filtering**: User selects filters → Results update without dialogue
3. **Suggestions**: User selects component → Backend queries Algolia to suggest compatible parts
4. **Analytics**: Algolia tracks searches and clicks to improve suggestions
5. **No Conversation**: All intelligence happens passively - no user needs to ask for help

## Project Features Aligned with Challenge

### Contextual Data Retrieval
- Components are retrieved based on user selections without explicit requests
- Algolia facets enable smart filtering
- Analytics drive better recommendations

### Fast & Relevant Results
- Algolia searches complete in <100ms
- Results sorted by relevance, price, and performance tier
- Facets enable narrowing down to exactly what user needs

### Non-Conversational UX
- Suggestions appear automatically as user builds
- Compatibility status shows instantly
- No chatbot or dialogue needed

## Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

### Manual Testing
1. Search for "Intel Core i9"
2. Select an i9 CPU
3. Notice compatible motherboards suggested
4. Select a motherboard
5. See compatible RAM suggested
6. Verify compatibility status shows all green
7. Check total price and power calculation

## Deployment

### Deploy to Production

**Backend (Railway):**
```bash
railway link [your-railway-project-id]
railway variables set ALGOLIA_APP_ID=your_id
railway up
```

**Frontend (Vercel):**
```bash
vercel --prod
```

## Algolia Setup Instructions

1. Sign up at [algolia.com](https://algolia.com)
2. Create application
3. Create index named `pc_components`
4. Configure facets: brand, type, socket, performance_tier
5. Upload component data (script provided in `/backend/data/upload.py`)
6. Copy Application ID and API keys to `.env`

## Project Structure
```
.
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── data/
│   │   └── components.json
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Known Limitations

- Component database contains 200+ popular components (limited by Algolia free tier)
- No case/cooling/peripherals (scope focused on core components)
- Prices are simplified (not real-time market prices)

## Future Enhancements

- Add case compatibility checking
- Integrate real PCPartPicker prices
- Add performance benchmarking
- Create build sharing/comparison
- Add GPU VRAM requirements analysis
- Integrate thermal and power draw analysis

## Support & Feedback

For issues or feedback, please [open an issue on GitHub](https://github.com/yourusername/pcbuild_assist/issues)

## License

MIT License - see LICENSE.md for details
```

### 7.2 Document API Endpoints

**API.md - Complete API Documentation**
```markdown
# PCBuild Assist API Documentation

## Base URL
```
Production: https://your-backend.railway.app/api
Development: http://localhost:5000/api
```

## Authentication
Currently no authentication required. In production, add API key validation.

## Components Endpoints

### Search Components
**GET** `/components/search`

Query Parameters:
- `q` (required): Search query string
- `component_type` (optional): Filter by CPU, GPU, RAM, Motherboard, PSU, Storage
- `max_price` (optional): Maximum price filter
- `brand` (optional): Filter by brand
- `limit` (optional): Results per page (default: 20, max: 100)
- `offset` (optional): Pagination offset (default: 0)

Example:
```bash
curl "http://localhost:5000/api/components/search?q=Intel+i9&component_type=CPU&max_price=1000"
```

Response:
```json
{
  "query": "Intel i9",
  "count": 5,
  "results": [
    {
      "id": "cpu_001",
      "name": "Intel Core i9-13900K",
      "brand": "Intel",
      "type": "CPU",
      "price": 589.99,
      "specs": {
        "cores": 24,
        "socket": "LGA1700",
        "tdp": 253
      }
    }
  ]
}
```

### Get Components by Type
**GET** `/components/type/{type}`

Path Parameters:
- `type`: CPU, GPU, RAM, Motherboard, PSU, or Storage

Query Parameters:
- `brand` (optional): Filter by brand
- `max_price` (optional): Maximum price
- `limit` (optional): Results to return

Example:
```bash
curl "http://localhost:5000/api/components/type/GPU?max_price=1500"
```

### Get Available Facets
**GET** `/components/facets`

Query Parameters:
- `component_type` (optional): Get facets for specific type

Response:
```json
{
  "available_filters": {
    "brand": ["Intel", "AMD", "NVIDIA", "Corsair", ...],
    "performance_tier": ["budget", "mid-range", "high-end"],
    "socket": ["LGA1700", "AM5", "TR40"],
    "memory_type": ["DDR4", "DDR5"]
  }
}
```

## Compatibility Endpoints

### Check Full Build Compatibility
**POST** `/compatibility/check-build`

Request Body:
```json
{
  "cpu_id": "cpu_001",
  "motherboard_id": "mb_001",
  "gpu_id": "gpu_001",
  "ram_id": "ram_001",
  "psu_id": "psu_001"
}
```

Response:
```json
{
  "compatible": true,
  "checks": [
    {
      "check": "CPU-Motherboard",
      "compatible": true,
      "message": "Compatible: Both use LGA1700"
    },
    {
      "check": "RAM-Motherboard",
      "compatible": true,
      "message": "Compatible: Both use DDR5"
    },
    {
      "check": "GPU-PSU",
      "compatible": true,
      "message": "Compatible: 850W PSU sufficient for 450W GPU"
    }
  ],
  "warnings": [],
  "total_power": 828
}
```

### Check Component Pair
**GET** `/compatibility/check-pair/{component1_id}/{component2_id}`

Response:
```json
{
  "compatible": true,
  "message": "Compatible: Both use LGA1700"
}
```

## Suggestions Endpoints

### Suggest CPUs
**GET** `/suggestions/cpus`

Query Parameters:
- `budget` (optional): Maximum budget in USD
- `use_case` (optional): gaming, streaming, workstation, budget

Example:
```bash
curl "http://localhost:5000/api/suggestions/cpus?budget=1500&use_case=gaming"
```

Response:
```json
{
  "suggestions": [
    {
      "id": "cpu_001",
      "name": "Intel Core i9-13900K",
      "price": 589.99,
      "specs": {...}
    }
  ],
  "count": 5
}
```

### Suggest Compatible GPU
**GET** `/suggestions/compatible-gpu/{cpu_id}`

Query Parameters:
- `budget` (optional): Maximum budget

Response:
```json
{
  "for_cpu": "Intel Core i9-13900K",
  "suggestions": [...],
  "count": 5
}
```

### Suggest Compatible Motherboard
**GET** `/suggestions/compatible-motherboard/{cpu_id}`

Response:
```json
{
  "for_cpu": "Intel Core i9-13900K",
  "suggestions": [
    {
      "id": "mb_001",
      "name": "ASUS ROG Maximus Z790",
      "socket": "LGA1700",
      "price": 389.99
    }
  ],
  "count": 5
}
```

### Suggest RAM
**GET** `/suggestions/ram/{motherboard_id}`

Query Parameters:
- `budget` (optional): Maximum budget

### Suggest PSU
**GET** `/suggestions/psu?total_power=600`

Query Parameters:
- `total_power` (required): Total system power in watts

Response:
```json
{
  "recommended_wattage": 750,
  "suggestions": [...],
  "count": 5
}
```

## Error Handling

### Error Response Format
```json
{
  "error": "Component not found",
  "detail": "No component with ID cpu_999 exists"
}
```

### HTTP Status Codes
- `200`: Success
- `400`: Bad request
- `404`: Not found
- `422`: Validation error
- `500`: Server error

## Rate Limiting

Currently unlimited. In production, implement:
- 100 requests per minute per IP
- Rate limit headers in response
```

### 7.3 Create User Guide

**USER_GUIDE.md**
```markdown
# PCBuild Assist - User Guide

## Getting Started

### 1. Home Page
- Click "Start Building" button to begin

### 2. Builder Interface

#### Left Panel: Search & Browse
1. **Search Bar**: Type component names or specs
   - Example: "Intel i9", "RTX 4090", "32GB DDR5"
2. **Component Type Tabs**: Switch between CPU, GPU, RAM, MB, PSU, Storage
3. **Filters**: Narrow by price, brand, performance tier
4. **Results**: Scroll through matching components

#### Right Panel: Your Build
- **Selected Components**: See what you've chosen
- **Total Price**: Real-time cost calculation
- **Total Power**: System wattage requirement
- **Compatibility Status**: ✓ Green = compatible, ✗ Red = issue
- **Suggestions**: Recommended components for next step

### 3. Building Your PC

**Step 1: Select CPU**
- Search "Intel Core i9" or "AMD Ryzen"
- Click "Select" on your choice
- Notice motherboards automatically suggested

**Step 2: Select Motherboard**
- Filter by CPU socket (LGA1700, AM5, etc)
- Choose based on features and price
- RAM suggestions update automatically

**Step 3: Select RAM**
- Filter by type (DDR4, DDR5) - must match motherboard
- Choose capacity (16GB, 32GB, 64GB)
- Speed usually doesn't matter much for gaming

**Step 4: Select GPU**
- Filter by performance tier and price
- Avoid bottlenecks - match GPU to CPU tier
- PSU requirements will show

**Step 5: Select PSU**
- Look for wattage recommended by system
- Gold+ efficiency recommended
- Modular cables make building easier

**Step 6: Add Storage**
- Add one or more SSDs/HDDs
- NVMe M.2 is fastest option
- Add multiple storage devices if needed

### 4. Compatibility Checking

**Green Checkmarks ✓**
- Component pairs are compatible
- No issues detected

**Red X Marks ✗**
- Components don't work together
- Example: DDR4 RAM with DDR5 motherboard
- Go back and select different component

**Warnings ⚠️**
- Components work but not optimal
- Example: Weak PSU for GPU
- Consider upgrading

### 5. Using Smart Suggestions

The app shows suggestions for next components automatically:
1. After selecting CPU → Motherboards suggested
2. After selecting MB → RAM suggested
3. After selecting CPU+GPU → PSU suggested

**Why?** These suggestions are verified compatible and well-matched for price/performance.

### 6. Saving Your Build

- Build automatically saves to your browser
- Returns next time you visit
- Share URL to show others your build
- Export build info (coming soon)

### 7. Tips & Tricks

**Budget Building ($800)**
- Start with mid-range CPU ($250-350)
- Match with mid-range GPU ($350-400)
- 16GB RAM ($60-80)
- 650W PSU ($60-80)

**High-End Gaming ($3000+)**
- High-end CPU ($500-700)
- High-end GPU ($1500-2000)
- 32GB RAM ($150-200)
- 1000W+ PSU ($200+)

**Avoid Common Mistakes**
- ❌ Don't pair high-end GPU with budget CPU → bottleneck
- ❌ Don't use 500W PSU with 450W GPU → not enough power
- ❌ Don't mix DDR4 RAM with DDR5 motherboard → incompatible
- ❌ Don't cheap out on PSU → damages components

**Find Great Deals**
- Search by performance tier, not model number
- Previous generation CPUs/GPUs often great value
- Filter by price to find sweet spots

## Frequently Asked Questions

**Q: What if I see a red X?**
A: These components don't work together. Select a different component.

**Q: Can I use DDR4 on a DDR5 motherboard?**
A: No. You must use the memory type the motherboard supports.

**Q: How much PSU wattage do I need?**
A: Add CPU TDP + GPU TDP, multiply by 1.25. Example: 125W + 450W = 575W, so get 720W+ PSU.

**Q: What's TDP?**
A: Thermal Design Power - how much electricity (in watts) the component uses.

**Q: Can I use AM5 CPU with LGA1700 motherboard?**
A: No. Socket must match exactly.

**Q: Is 32GB RAM overkill?**
A: For gaming: 16GB fine. For streaming/3D rendering: 32GB+ recommended.

## Contact & Support

Issues or questions? Email support@pcbuilder.app or open an issue on GitHub.
```

### 7.4 Prepare Algolia Submission Post

**Create Submission Post Template**
```markdown
# PCBuild Assist: Smart Component Selection Without Conversation

## Challenge Submission: Consumer-Facing Non-Conversational Experience

### Project Overview
PCBuild Assist demonstrates how contextual data retrieval through Algolia enhances user experience without requiring back-and-forth dialogue. Users select PC components and receive intelligent, compatible recommendations automatically.

### Problem Solved
PC building is complex - components have intricate compatibility rules. Users need:
- Fast access to thousands of components
- Instant compatibility validation
- Smart suggestions for next components
- Zero friction - no questions asked

### Algolia Solution

**1. Fast Component Search**
- Users type "RTX 4090" → Get results in <100ms via Algolia
- Faceted search enables instant filtering by brand, price, performance

**2. Contextual Suggestions**
- User selects Intel i9-13900K (LGA1700)
- Backend queries Algolia for motherboards with socket:LGA1700
- Suggestions appear automatically - no conversation needed

**3. Compatibility Without Conversation**
- Build validates automatically as components added
- Uses Algolia data to check socket, RAM type, PCIe version
- Color-coded indicators (✓/✗) show compatibility instantly

**4. Analytics-Driven Insights**
- Algolia analytics track popular searches
- Click analytics show which components users prefer
- Data informs suggestion rankings

### Key Features

1. **Real-time Search**: Type to instantly find components
2. **Smart Filtering**: Brand, price, performance tier, socket
3. **Contextual Suggestions**: Auto-suggest compatible components
4. **Instant Validation**: Color-coded compatibility status
5. **Price Calculation**: Total build cost updates live
6. **Power Analysis**: System wattage requirements
7. **Non-conversational**: All intelligence passive - no user needs to ask

### Technical Implementation

**Architecture:**
- React frontend (UI/search)
- Python FastAPI backend (compatibility logic)
- Algolia (component search, analytics)
- PostgreSQL (source data)

**Algolia Integration:**
- Index: ~300 PC components
- Facets: Brand, type, socket, DDR version, performance tier
- Custom ranking: Relevance, price, recency
- Analytics enabled for insights

### Results

✓ Search <100ms across 300+ components
✓ Faceted filtering for precise results
✓ Zero user friction - suggestions automatic
✓ 100% accuracy on compatibility checks
✓ Analytics-driven recommendations

### How It Works

1. User searches "gaming PC CPU budget"
2. Algolia returns relevant CPUs ranked by value
3. User selects i9-13900K
4. System queries Algolia for compatible motherboards
5. Suggestions appear in UI (no conversation)
6. User selects motherboard
7. RAM, PSU suggestions auto-update
8. Full build validates instantly
9. Compatible ✓ or changes needed indicator shown

### Non-Conversational Excellence

This isn't a chatbot or Q&A interface. Instead:
- **Search replaces "What CPUs do you have?"**
- **Filtering replaces "Show me gaming CPUs under $500"**
- **Suggestions replace "What motherboard works with this CPU?"**
- **Validation replaces "Will these components work together?"**

All intelligence happens passively through Algolia's fast data retrieval.

### Deployment

- **Frontend**: Vercel
- **Backend**: Railway  
- **URL**: [your-deployed-url]
- **Demo Video**: [link to demo]

### Judge Testing Instructions

1. Visit the live demo
2. Search for "Intel" - see instant results
3. Select an i9 CPU
4. Notice compatible motherboards suggested
5. Select a motherboard
6. See RAM suggestions update
7. Build full PC and verify compatibility checks
8. Change a component to see red X warning
9. Use filters to narrow down options

No credentials needed - everything works publicly.

### Algolia Features Used

- ✓ Multiple Indexes
- ✓ Faceted Search
- ✓ Custom Ranking
- ✓ Analytics
- ✓ Synonyms
- ✓ Typo Tolerance
- ✓ Pagination

### Conclusion

PCBuild Assist showcases how Algolia's fast, relevant search transforms the user experience. By eliminating conversational friction and providing instant, contextual information, we created an intuitive tool that Just Works™.

---

**Submission URLs:**
- Live App: https://your-app.vercel.app
- GitHub: https://github.com/yourusername/pcbuild_assist
- API Docs: https://your-api.railway.app/docs
```

### 7.5 Pre-Submission Checklist

- [ ] README with setup instructions
- [ ] API documentation complete
- [ ] User guide with examples
- [ ] Submission post written
- [ ] Live demo working
- [ ] All tests passing
- [ ] No console errors
- [ ] Performance good (<200ms searches)
- [ ] Algolia index populated
- [ ] Deployment URLs working
- [ ] GitHub repo public
- [ ] License included (MIT)
- [ ] Demo video recorded (optional)

### 7.6 Test Judge Experience

1. Visit your live app
2. Follow the user guide from their perspective
3. Record any friction points
4. Fix issues found
5. Test on mobile
6. Test with slow network (DevTools throttle)
7. Verify all links work
8. Check that Algolia clearly integrated

### 7.7 Submit Project

**Submit to Algolia:**
1. Go to challenge submission page
2. Fill in project details
3. Upload submission post (Markdown)
4. Provide live app URL
5. Provide GitHub repo URL
6. Submit!

**Post on Social Media:**
- Twitter: Share with #AlgoliaChallenge
- LinkedIn: Announce project
- GitHub: Release version 1.0

### 7.8 Post-Submission

- Monitor feedback
- Fix any bugs judges report
- Be ready for questions
- Prepare demo for live showcase (if selected)

## Key Features to Implement
- **Proactive Suggestions**: Real-time component recommendations based on selections
- **Compatibility Checking**: Instant validation of component compatibility
- **Smart Filtering**: Dynamic filtering based on budget, performance, or use case
- **Performance Optimization**: Fast Algolia queries for instant results
- **User-Friendly**: No explicit conversation required—suggestions appear contextually

## Technology Stack (Recommended)
- **Frontend**: React
- **Backend**: Python (FastAPI)
- **Search**: Algolia Agent Studio
- **Hosting**: Vercel (frontend), Railway (backend)
- **Database**: PostgreSQL or MongoDB for source data

## Success Criteria
- ✓ Functional PC builder with component selection
- ✓ Real-time compatibility checking
- ✓ Proactive smart suggestions via Algolia
- ✓ Deployed and accessible online
- ✓ Performance optimized queries
- ✓ Clear documentation for judges
- ✓ Submission post published using template

## Notes
- Start with minimal viable product (MVP)
- Focus on user experience for non-conversational interaction
- Ensure Algolia integration is clearly demonstrated
- Test thoroughly before deployment
