from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.algolia_service import algolia_service
from app.models.component import ComponentResponse

router = APIRouter()

@router.get("/search")
async def search_components(
    q: str = Query(..., min_length=1, description="Search query"),
    component_type: Optional[str] = Query(None, description="Filter by type: CPU, GPU, RAM, Motherboard, etc."),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    Search PC components with Algolia
    Returns matching components with scores and highlights
    """
    filters = {}
    
    if component_type:
        filters["type"] = component_type
    
    if brand:
        filters["brand"] = brand
    
    if max_price or min_price:
        filters["price_range"] = {
            "min": min_price or 0,
            "max": max_price or 999999
        }
    
    try:
        results = algolia_service.search_components(q, filters=filters, limit=limit, offset=offset)
        
        return {
            "query": q,
            "count": results.get("nbHits", 0),
            "page": results.get("page", 0),
            "totalPages": results.get("nbPages", 0),
            "results": results.get("hits", []),
            "filters_applied": filters,
            "processing_time_ms": results.get("processingTimeMS", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/type/{component_type}")
async def get_by_type(
    component_type: str,
    brand: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None, ge=0),
    socket: Optional[str] = Query(None, description="Filter by socket (for CPUs/Motherboards)"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get all components of a specific type with optional filters
    """
    filters = {}
    
    if brand:
        filters["brand"] = brand
    
    if max_price:
        filters["price_range"] = {"min": 0, "max": max_price}
    
    if socket:
        filters["socket"] = socket
    
    try:
        results = algolia_service.search_by_type(component_type, filters=filters, limit=limit)
        
        return {
            "type": component_type,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching components: {str(e)}")

@router.get("/facets")
async def get_facets(
    component_type: Optional[str] = Query(None, description="Optional type filter")
):
    """
    Get available filter options (brands, tiers, sockets, etc.)
    Useful for populating filter dropdowns in UI
    """
    try:
        facets = algolia_service.get_facets(component_type)
        
        return {
            "component_type": component_type,
            "available_filters": facets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching facets: {str(e)}")

@router.get("/{component_id}")
async def get_component_details(component_id: str):
    """
    Get detailed info about a specific component
    """
    try:
        component = algolia_service.get_component_by_id(component_id)
        
        if not component:
            raise HTTPException(status_code=404, detail="Component not found")
        
        return component
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching component: {str(e)}")
