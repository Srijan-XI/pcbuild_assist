from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import date

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

# ==================== ENHANCED DATA MODELS ====================

class ComponentRating(BaseModel):
    """User rating data for components"""
    average: float = Field(0.0, ge=0, le=5, description="Average rating (0-5 stars)")
    count: int = Field(0, ge=0, description="Number of ratings")
    distribution: Optional[Dict[str, int]] = Field(None, description="Rating distribution by star count")

class PriceHistory(BaseModel):
    """Price tracking data"""
    current: float = Field(..., description="Current price")
    lowest_30d: Optional[float] = Field(None, description="Lowest price in last 30 days")
    highest_30d: Optional[float] = Field(None, description="Highest price in last 30 days")
    average_30d: Optional[float] = Field(None, description="Average price in last 30 days")
    last_updated: Optional[str] = Field(None, description="Last price update timestamp")
    trend: Optional[str] = Field(None, description="Price trend: rising, falling, stable")

class BenchmarkScores(BaseModel):
    """Performance benchmark data"""
    single_core: Optional[int] = Field(None, description="Single-core performance score")
    multi_core: Optional[int] = Field(None, description="Multi-core performance score")
    gaming_fps_1080p: Optional[int] = Field(None, description="Average FPS at 1080p gaming")
    gaming_fps_1440p: Optional[int] = Field(None, description="Average FPS at 1440p gaming")
    gaming_fps_4k: Optional[int] = Field(None, description="Average FPS at 4K gaming")
    productivity_score: Optional[int] = Field(None, description="Productivity workload score")
    power_efficiency: Optional[float] = Field(None, description="Performance per watt ratio")

class CompatibilityNotes(BaseModel):
    """Known compatibility issues or notes"""
    requires_bios_update: Optional[bool] = Field(False, description="Requires BIOS update for some boards")
    bios_version: Optional[str] = Field(None, description="Minimum BIOS version required")
    known_issues: Optional[List[str]] = Field(None, description="List of known compatibility issues")
    recommended_with: Optional[List[str]] = Field(None, description="Components it pairs well with")

class ComponentMetrics(BaseModel):
    """Computed metrics for smart suggestions"""
    value_score: Optional[float] = Field(None, description="Price-to-performance ratio (0-100)")
    popularity_score: Optional[float] = Field(None, description="Community popularity (0-100)")
    future_proof_score: Optional[float] = Field(None, description="Longevity/upgrade potential (0-100)")
    recommendation_score: Optional[float] = Field(None, description="Overall recommendation score (0-100)")

class Component(ComponentBase):
    """Full component model"""
    id: str
    type: str = Field(..., description="Component type (CPU, GPU, Motherboard, etc.)")
    brand: Optional[str] = None
    specs: Optional[Dict[str, Any]] = {}
    compatibility: Optional[Dict[str, Any]] = {}
    performance_tier: Optional[str] = Field(None, description="high-end, mid-range, or budget")
    release_year: Optional[int] = None
    
    # Enhanced data fields
    release_date: Optional[str] = Field(None, description="Release date (YYYY-MM-DD)")
    rating: Optional[ComponentRating] = Field(None, description="User ratings")
    price_history: Optional[PriceHistory] = Field(None, description="Price tracking data")
    benchmarks: Optional[BenchmarkScores] = Field(None, description="Performance benchmarks")
    compatibility_notes: Optional[CompatibilityNotes] = Field(None, description="Compatibility information")
    metrics: Optional[ComponentMetrics] = Field(None, description="Computed recommendation metrics")
    stock_status: Optional[str] = Field(None, description="in-stock, low-stock, out-of-stock, pre-order")
    retailer_links: Optional[Dict[str, str]] = Field(None, description="Links to retailers")

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
