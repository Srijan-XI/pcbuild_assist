from fastapi import APIRouter, Query, Request
from typing import Optional
import time

from app.services.algolia_service import algolia_service
from app.models.component import ComponentResponse
from app.core.exceptions import NotFoundException, ValidationException, AlgoliaException
from app.core.responses import success_response, paginated_response
from app.core.cache import cached, cache
from app.core.logging import get_logger, get_request_id
from app.core.rate_limit import limiter

router = APIRouter()
logger = get_logger(__name__)


@router.get("/search")
@limiter.limit("30/minute")
async def search_components(
    request: Request,
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    component_type: Optional[str] = Query(None, description="Filter by type: CPU, GPU, RAM, Motherboard, etc."),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    max_price: Optional[float] = Query(None, ge=0, le=100000, description="Maximum price"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    performance_tier: Optional[str] = Query(None, description="Filter by tier: budget, mid-range, high-end"),
    sort_by: Optional[str] = Query(None, description="Sort by: price_asc, price_desc, name, relevance"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    page: int = Query(0, ge=0, description="Page number (0-indexed)")
):
    """
    Search PC components with Algolia.
    
    Returns matching components with scores and highlights.
    Results are cached for 5 minutes.
    
    **Rate Limit:** 30 requests/minute
    """
    start_time = time.perf_counter()
    
    # Validate price range
    if min_price and max_price and min_price > max_price:
        raise ValidationException(
            message="min_price cannot be greater than max_price",
            field="price_range"
        )
    
    # Build filters
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
    if performance_tier:
        filters["performance_tier"] = performance_tier
    
    logger.info(f"Searching components: '{q}'", data={
        "query": q,
        "filters": filters,
        "limit": limit,
        "page": page
    })
    
    try:
        results = algolia_service.search_components(
            q, 
            filters=filters, 
            limit=limit, 
            offset=page * limit
        )
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return paginated_response(
            data=results.get("hits", []),
            page=page,
            per_page=limit,
            total_items=results.get("nbHits", 0),
            request_id=get_request_id(),
            processing_time_ms=process_time,
            query=q,
            filters=filters
        )
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}", data={"query": q, "error": str(e)})
        raise AlgoliaException(operation="search", message=str(e))


@router.get("/type/{component_type}")
@limiter.limit("60/minute")
async def get_by_type(
    request: Request,
    component_type: str,
    brand: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None, ge=0),
    min_price: Optional[float] = Query(None, ge=0),
    socket: Optional[str] = Query(None, description="Filter by socket (for CPUs/Motherboards)"),
    performance_tier: Optional[str] = Query(None, description="Filter by tier: budget, mid-range, high-end"),
    sort_by: Optional[str] = Query("price_asc", description="Sort: price_asc, price_desc, name"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get components of a specific type with optional filters.
    
    Supported types: CPU, GPU, Motherboard, Memory, Power Supply, Internal Hard Drive
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    # Validate component type
    valid_types = ["CPU", "GPU", "Motherboard", "Memory", "Power Supply", "Internal Hard Drive", "Video Card"]
    if component_type not in valid_types:
        logger.warning(f"Unknown component type requested: {component_type}")
        # Don't error - Algolia will handle it
    
    filters = {}
    if brand:
        filters["brand"] = brand
    if max_price or min_price:
        filters["price_range"] = {"min": min_price or 0, "max": max_price or 999999}
    if socket:
        filters["socket"] = socket
    if performance_tier:
        filters["performance_tier"] = performance_tier
    
    try:
        results = algolia_service.search_by_type(component_type, filters=filters, limit=limit)
        
        # Apply sorting
        if sort_by == "price_asc":
            results.sort(key=lambda x: x.get("price", 999999))
        elif sort_by == "price_desc":
            results.sort(key=lambda x: x.get("price", 0), reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda x: x.get("name", ""))
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "type": component_type,
                "count": len(results),
                "results": results,
                "filters_applied": filters
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
        
    except Exception as e:
        logger.error(f"Get by type failed: {str(e)}", data={"type": component_type})
        raise AlgoliaException(operation="search_by_type", message=str(e))


@router.get("/facets")
@limiter.limit("30/minute")
async def get_facets(
    request: Request,
    component_type: Optional[str] = Query(None, description="Optional type filter")
):
    """
    Get available filter options (brands, tiers, sockets, etc.)
    
    Useful for populating filter dropdowns in UI.
    Results are cached for 30 minutes.
    
    **Rate Limit:** 30 requests/minute
    """
    start_time = time.perf_counter()
    
    # Check cache first
    cache_key = f"facets:{component_type or 'all'}"
    cached_result = cache.get("facets", cache_key)
    if cached_result:
        return success_response(
            data=cached_result,
            request_id=get_request_id(),
            processing_time_ms=0
        )
    
    try:
        facets = algolia_service.get_facets(component_type)
        
        # Cache the result
        cache.set("facets", cache_key, facets)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "component_type": component_type,
                "available_filters": facets
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
        
    except Exception as e:
        logger.error(f"Get facets failed: {str(e)}")
        raise AlgoliaException(operation="get_facets", message=str(e))


@router.get("/popular")
@limiter.limit("60/minute")
async def get_popular_components(
    request: Request,
    component_type: Optional[str] = Query(None, description="Filter by component type"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get popular/trending components.
    
    Returns top-rated and frequently selected components.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        filters = {}
        if component_type:
            filters["type"] = component_type
        
        # Search with empty query to get all, sorted by popularity
        results = algolia_service.search_components("", filters=filters, limit=limit)
        
        # Sort by recommendation score if available, else by rating
        hits = results.get("hits", [])
        hits.sort(
            key=lambda x: (
                x.get("recommendation_score", 0),
                x.get("rating", {}).get("average", 0) if isinstance(x.get("rating"), dict) else 0
            ),
            reverse=True
        )
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "component_type": component_type,
                "count": len(hits[:limit]),
                "results": hits[:limit]
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
        
    except Exception as e:
        logger.error(f"Get popular failed: {str(e)}")
        raise AlgoliaException(operation="get_popular", message=str(e))


@router.get("/{component_id}")
@limiter.limit("100/minute")
async def get_component_details(
    request: Request,
    component_id: str
):
    """
    Get detailed info about a specific component.
    
    Results are cached for 10 minutes.
    
    **Rate Limit:** 100 requests/minute
    """
    start_time = time.perf_counter()
    
    # Check cache
    cache_key = f"component:{component_id}"
    cached_result = cache.get("components", cache_key)
    if cached_result:
        return success_response(
            data=cached_result,
            request_id=get_request_id(),
            processing_time_ms=0
        )
    
    try:
        component = algolia_service.get_component_by_id(component_id)
        
        if not component:
            raise NotFoundException(resource="Component", identifier=component_id)
        
        # Cache the result
        cache.set("components", cache_key, component)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data=component,
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
        
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"Get component failed: {str(e)}", data={"component_id": component_id})
        raise AlgoliaException(operation="get_component", message=str(e))

