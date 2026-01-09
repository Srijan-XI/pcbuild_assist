from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any

class ComponentBase(BaseModel):
    """Base component model"""
    name: str
    price: Optional[float] = None
    
class CPUSpecs(BaseModel):
    """CPU specifications"""
    core_count: Optional[int] = None
    core_clock: Optional[str] = None
    boost_clock: Optional[str] = None
    microarchitecture: Optional[str] = None
    tdp: Optional[int] = None
    graphics: Optional[str] = None

class MotherboardSpecs(BaseModel):
    """Motherboard specifications"""
    socket: Optional[str] = None
    form_factor: Optional[str] = None
    max_memory: Optional[int] = None
    memory_slots: Optional[int] = None
    color: Optional[str] = None

class Component(ComponentBase):
    """Full component model"""
    id: str
    type: str = Field(..., description="Component type (CPU, GPU, Motherboard, etc.)")
    brand: Optional[str] = None
    specs: Optional[Dict[str, Any]] = {}
    compatibility: Optional[Dict[str, Any]] = {}
    performance_tier: Optional[str] = Field(None, description="high-end, mid-range, or budget")
    release_year: Optional[int] = None

class ComponentResponse(Component):
    """Component with search metadata"""
    search_score: Optional[float] = None
    _highlightResult: Optional[Dict] = None

class SearchRequest(BaseModel):
    """Search request parameters"""
    query: str = Field(..., min_length=1, description="Search query string")
    component_type: Optional[str] = Field(None, description="Filter by component type")
    brand: Optional[str] = None
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    performance_tier: Optional[str] = None
    limit: int = Field(20, ge=1, le=100, description="Maximum results to return")
    offset: int = Field(0, ge=0, description="Pagination offset")

class SearchFilters(BaseModel):
    """Advanced search filters"""
    facet_filters: Optional[List[str]] = None
    numeric_filters: Optional[List[str]] = None

class CompatibilityCheck(BaseModel):
    """Compatibility check result"""
    check_name: str
    compatible: bool
    message: str
    severity: str = Field("error", description="error, warning, or info")

class BuildCompatibilityRequest(BaseModel):
    """Request to check build compatibility"""
    cpu_id: Optional[str] = None
    motherboard_id: Optional[str] = None
    gpu_id: Optional[str] = None
    ram_id: Optional[str] = None
    psu_id: Optional[str] = None
    storage_ids: Optional[List[str]] = []

class BuildCompatibilityResponse(BaseModel):
    """Build compatibility check response"""
    compatible: bool
    checks: List[CompatibilityCheck]
    warnings: List[str] = []
    total_power: int = Field(0, description="Total system power consumption in watts")
    recommended_psu: int = Field(0, description="Recommended PSU wattage")

class SuggestionRequest(BaseModel):
    """Request for component suggestions"""
    component_id: str
    budget: Optional[float] = None
    use_case: Optional[str] = Field(None, description="gaming, streaming, workstation, etc.")

class SuggestionResponse(BaseModel):
    """Component suggestions response"""
    for_component: str
    suggestions: List[Component]
    count: int
    reasoning: Optional[str] = None
