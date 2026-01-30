from fastapi import APIRouter, Query, Request
from typing import Optional, List
import time

from app.services.suggestion_service import suggestion_service, ComponentScorer
from app.services.algolia_service import algolia_service
from app.core.exceptions import NotFoundException, ValidationException, AlgoliaException
from app.core.responses import success_response
from app.core.cache import cache
from app.core.logging import get_logger, get_request_id
from app.core.rate_limit import limiter

router = APIRouter()
logger = get_logger(__name__)


@router.get("/cpus")
@limiter.limit("60/minute")
async def suggest_cpus(
    request: Request,
    budget: Optional[float] = Query(None, ge=0, le=10000, description="Maximum budget"),
    use_case: Optional[str] = Query(None, description="gaming, streaming, workstation, etc."),
    limit: int = Query(10, ge=1, le=20)
):
    """
    Get CPU suggestions based on budget and use case.
    
    Uses multi-factor scoring to recommend best CPUs.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        suggestions = suggestion_service.suggest_cpus(budget=budget, use_case=use_case, limit=limit)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "budget": budget,
                "use_case": use_case,
                "suggestions": suggestions,
                "count": len(suggestions)
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except Exception as e:
        logger.error(f"CPU suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_cpus", message=str(e))


@router.get("/compatible-gpu/{cpu_id}")
@limiter.limit("60/minute")
async def suggest_compatible_gpu(
    request: Request,
    cpu_id: str,
    budget: Optional[float] = Query(None, ge=0, le=10000)
):
    """
    Suggest GPUs compatible and balanced with selected CPU.
    
    Matches performance tiers to avoid bottlenecks.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        cpu = algolia_service.get_component_by_id(cpu_id)
        if not cpu:
            raise NotFoundException(resource="CPU", identifier=cpu_id)
        
        suggestions = suggestion_service.suggest_compatible_gpu(cpu, budget=budget)
        cpu_tier = cpu.get("performance_tier", "mid-range")
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "for_cpu": {
                    "id": cpu_id,
                    "name": cpu.get("name"),
                    "tier": cpu_tier
                },
                "suggestions": suggestions,
                "count": len(suggestions),
                "reasoning": f"GPUs balanced for {cpu_tier} CPU to avoid bottlenecks"
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"GPU suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_compatible_gpu", message=str(e))


@router.get("/compatible-motherboard/{cpu_id}")
@limiter.limit("60/minute")
async def suggest_compatible_motherboard(
    request: Request,
    cpu_id: str
):
    """
    Suggest motherboards compatible with CPU socket.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        cpu = algolia_service.get_component_by_id(cpu_id)
        if not cpu:
            raise NotFoundException(resource="CPU", identifier=cpu_id)
        
        suggestions = suggestion_service.suggest_compatible_motherboard(cpu)
        cpu_socket = cpu.get("specs", {}).get("socket") or cpu.get("socket", "unknown")
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "for_cpu": {
                    "id": cpu_id,
                    "name": cpu.get("name"),
                    "socket": cpu_socket
                },
                "suggestions": suggestions,
                "count": len(suggestions),
                "reasoning": f"Motherboards with {cpu_socket} socket"
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"Motherboard suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_compatible_motherboard", message=str(e))


@router.get("/ram/{motherboard_id}")
@limiter.limit("60/minute")
async def suggest_ram(
    request: Request,
    motherboard_id: str,
    budget: Optional[float] = Query(None, ge=0, le=2000)
):
    """
    Suggest RAM compatible with motherboard memory type.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        motherboard = algolia_service.get_component_by_id(motherboard_id)
        if not motherboard:
            raise NotFoundException(resource="Motherboard", identifier=motherboard_id)
        
        suggestions = suggestion_service.suggest_ram(motherboard, budget=budget)
        mb_memory_type = motherboard.get("specs", {}).get("memory_type") or motherboard.get("memory_type", "unknown")
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "for_motherboard": {
                    "id": motherboard_id,
                    "name": motherboard.get("name"),
                    "memory_type": mb_memory_type
                },
                "suggestions": suggestions,
                "count": len(suggestions),
                "reasoning": f"RAM compatible with {mb_memory_type}"
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"RAM suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_ram", message=str(e))


@router.get("/psu")
@limiter.limit("60/minute")
async def suggest_psu(
    request: Request,
    total_power: int = Query(..., ge=100, le=2000, description="Total system power in watts"),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Suggest PSU based on system power requirements.
    
    Recommends PSU with 1.25x headroom for efficiency and future upgrades.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        suggestions = suggestion_service.suggest_psu(total_power, limit=limit)
        recommended_wattage = int(total_power * 1.25)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "total_power": total_power,
                "recommended_wattage": recommended_wattage,
                "suggestions": suggestions,
                "count": len(suggestions),
                "reasoning": f"PSU with ≥{recommended_wattage}W for {total_power}W system (25% headroom)"
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except Exception as e:
        logger.error(f"PSU suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_psu", message=str(e))


@router.get("/storage")
@limiter.limit("60/minute")
async def suggest_storage(
    request: Request,
    budget: Optional[float] = Query(None, ge=0, le=2000),
    capacity_gb: Optional[int] = Query(None, ge=0, le=20000),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Suggest storage options based on budget and capacity.
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        suggestions = suggestion_service.suggest_storage(
            budget=budget,
            capacity_gb=capacity_gb,
            limit=limit
        )
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "budget": budget,
                "capacity_gb": capacity_gb,
                "suggestions": suggestions,
                "count": len(suggestions)
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except Exception as e:
        logger.error(f"Storage suggestion failed: {str(e)}")
        raise AlgoliaException(operation="suggest_storage", message=str(e))


@router.get("/score/{component_id}")
@limiter.limit("100/minute")
async def get_component_score(
    request: Request,
    component_id: str,
    target_tier: str = Query("mid-range", description="Target performance tier for scoring")
):
    """
    Get detailed recommendation scores for a specific component.
    
    Returns multi-factor scoring breakdown including:
    - Tier match (25%): How well it fits the target tier
    - Value score (25%): Price-to-performance ratio
    - Popularity (20%): Reviews and ratings
    - Power efficiency (15%): Performance per watt
    - Future proof (15%): Longevity factors
    
    **Rate Limit:** 100 requests/minute
    """
    start_time = time.perf_counter()
    
    # Validate target tier
    valid_tiers = ["budget", "mid-range", "high-end"]
    if target_tier not in valid_tiers:
        raise ValidationException(
            message=f"Invalid tier. Must be one of: {valid_tiers}",
            field="target_tier"
        )
    
    try:
        component = algolia_service.get_component_by_id(component_id)
        if not component:
            raise NotFoundException(resource="Component", identifier=component_id)
        
        component_type = component.get("type", "Unknown")
        scores = ComponentScorer.calculate_total_score(component, component_type, target_tier)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "component_id": component_id,
                "component_name": component.get("name"),
                "component_type": component_type,
                "target_tier": target_tier,
                "total_score": scores["total"],
                "score_breakdown": scores["breakdown"],
                "scoring_weights": ComponentScorer.WEIGHTS,
                "interpretation": _interpret_score(scores["total"])
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except (NotFoundException, ValidationException):
        raise
    except Exception as e:
        logger.error(f"Component scoring failed: {str(e)}")
        raise AlgoliaException(operation="score_component", message=str(e))


def _interpret_score(score: float) -> dict:
    """Interpret a score into human-readable format."""
    if score >= 80:
        return {"rating": "Excellent", "description": "Highly recommended for this tier", "emoji": "🏆"}
    elif score >= 60:
        return {"rating": "Good", "description": "Solid choice with good value", "emoji": "✅"}
    elif score >= 40:
        return {"rating": "Average", "description": "Acceptable but better options exist", "emoji": "⚠️"}
    else:
        return {"rating": "Poor", "description": "Not recommended for this tier", "emoji": "❌"}


@router.post("/batch-score")
@limiter.limit("20/minute")
async def batch_score_components(
    request: Request,
    component_ids: List[str],
    target_tier: str = Query("mid-range", description="Target performance tier")
):
    """
    Score multiple components at once for comparison.
    
    Useful for quickly comparing options. Limited to 10 components.
    
    **Rate Limit:** 20 requests/minute (expensive operation)
    """
    start_time = time.perf_counter()
    
    if len(component_ids) > 10:
        raise ValidationException(
            message="Maximum 10 components per batch score request",
            field="component_ids"
        )
    
    if not component_ids:
        raise ValidationException(
            message="At least one component ID is required",
            field="component_ids"
        )
    
    try:
        results = []
        for comp_id in component_ids:
            component = algolia_service.get_component_by_id(comp_id)
            if component:
                component_type = component.get("type", "Unknown")
                scores = ComponentScorer.calculate_total_score(component, component_type, target_tier)
                results.append({
                    "id": comp_id,
                    "name": component.get("name"),
                    "type": component_type,
                    "price": component.get("price"),
                    "total_score": scores["total"],
                    "breakdown": scores["breakdown"],
                    "interpretation": _interpret_score(scores["total"])
                })
        
        # Sort by score
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "target_tier": target_tier,
                "components": results,
                "count": len(results),
                "best_pick": results[0] if results else None
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Batch scoring failed: {str(e)}")
        raise AlgoliaException(operation="batch_score", message=str(e))


@router.get("/preset/{preset_id}")
@limiter.limit("30/minute")
async def get_preset_suggestions(
    request: Request,
    preset_id: str,
    limit: int = Query(3, ge=1, le=5)
):
    """
    Get component suggestions for a build preset.
    
    Available presets:
    - **budget-gaming**: Great 1080p gaming under $800
    - **mid-range-gaming**: Solid 1440p performance ~$1200  
    - **high-end-gaming**: 4K gaming & streaming $2000+
    - **workstation**: Content creation & productivity
    
    **Rate Limit:** 30 requests/minute
    """
    start_time = time.perf_counter()
    
    presets = {
        "budget-gaming": {
            "budget": 800,
            "tier": "budget",
            "description": "Great 1080p gaming under $800",
            "target_resolution": "1080p",
            "target_fps": "60+"
        },
        "mid-range-gaming": {
            "budget": 1200,
            "tier": "mid-range", 
            "description": "Solid 1440p performance ~$1200",
            "target_resolution": "1440p",
            "target_fps": "60-144"
        },
        "high-end-gaming": {
            "budget": 2500,
            "tier": "high-end",
            "description": "4K gaming & streaming $2000+",
            "target_resolution": "4K",
            "target_fps": "60-120"
        },
        "workstation": {
            "budget": 3000,
            "tier": "high-end",
            "description": "Content creation & productivity",
            "target_resolution": "Multi-monitor",
            "use_case": "productivity"
        }
    }
    
    preset = presets.get(preset_id)
    if not preset:
        raise NotFoundException(
            resource="Preset",
            identifier=preset_id,
            message=f"Available presets: {list(presets.keys())}"
        )
    
    try:
        # Get suggested components for each category
        budget_per_component = {
            "CPU": preset["budget"] * 0.20,
            "GPU": preset["budget"] * 0.35,
            "Motherboard": preset["budget"] * 0.15,
            "Memory": preset["budget"] * 0.10,
            "Storage": preset["budget"] * 0.10,
            "PSU": preset["budget"] * 0.10
        }
        
        suggestions = {}
        total_estimated = 0
        
        for component_type, budget in budget_per_component.items():
            if component_type == "CPU":
                suggestions["CPU"] = suggestion_service.suggest_cpus(budget=budget, limit=limit)
            elif component_type == "Memory":
                results = algolia_service.search_by_type("Memory", filters={"price_range": {"min": 0, "max": budget}}, limit=limit * 2)
                scored = []
                for r in results:
                    s = ComponentScorer.calculate_total_score(r, "Memory", preset["tier"])
                    r["recommendation_score"] = s["total"]
                    scored.append(r)
                scored.sort(key=lambda x: x.get("recommendation_score", 0), reverse=True)
                suggestions["Memory"] = scored[:limit]
            elif component_type == "Storage":
                suggestions["Storage"] = suggestion_service.suggest_storage(budget=budget, limit=limit)
            elif component_type == "PSU":
                power_estimates = {"budget": 350, "mid-range": 500, "high-end": 700}
                suggestions["PSU"] = suggestion_service.suggest_psu(power_estimates.get(preset["tier"], 500), limit=limit)
            else:
                results = algolia_service.search_by_type(component_type, filters={"price_range": {"min": 0, "max": budget}}, limit=limit * 2)
                scored = []
                for r in results:
                    s = ComponentScorer.calculate_total_score(r, component_type, preset["tier"])
                    r["recommendation_score"] = s["total"]
                    scored.append(r)
                scored.sort(key=lambda x: x.get("recommendation_score", 0), reverse=True)
                suggestions[component_type] = scored[:limit]
            
            # Calculate estimated total from top picks
            if suggestions.get(component_type) and len(suggestions[component_type]) > 0:
                top_pick = suggestions[component_type][0]
                total_estimated += top_pick.get("price", 0)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "preset_id": preset_id,
                "preset_info": preset,
                "budget_allocation": budget_per_component,
                "suggestions": suggestions,
                "estimated_total": round(total_estimated, 2)
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"Preset suggestions failed: {str(e)}")
        raise AlgoliaException(operation="preset_suggestions", message=str(e))

