from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.suggestion_service import suggestion_service
from app.services.algolia_service import algolia_service

router = APIRouter()

@router.get("/cpus")
async def suggest_cpus(
    budget: Optional[float] = Query(None, ge=0),
    use_case: Optional[str] = Query(None, description="gaming, streaming, workstation, etc."),
    limit: int = Query(10, ge=1, le=20)
):
    """
    Get CPU suggestions based on budget and use case
    """
    try:
        suggestions = suggestion_service.suggest_cpus(budget=budget, use_case=use_case, limit=limit)
        
        return {
            "budget": budget,
            "use_case": use_case,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/compatible-gpu/{cpu_id}")
async def suggest_compatible_gpu(
    cpu_id: str,
    budget: Optional[float] = Query(None, ge=0)
):
    """
    Suggest GPUs compatible and balanced with selected CPU
    Matches performance tiers to avoid bottlenecks
    """
    try:
        cpu = algolia_service.get_component_by_id(cpu_id)
        if not cpu:
            raise HTTPException(status_code=404, detail="CPU not found")
        
        suggestions = suggestion_service.suggest_compatible_gpu(cpu, budget=budget)
        
        return {
            "for_cpu": cpu.get("name"),
            "cpu_tier": cpu.get("performance_tier", "unknown"),
            "suggestions": suggestions,
            "count": len(suggestions),
            "reasoning": f"GPUs balanced for {cpu.get('performance_tier', 'mid-range')} CPU"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/compatible-motherboard/{cpu_id}")
async def suggest_compatible_motherboard(cpu_id: str):
    """
    Suggest motherboards compatible with CPU socket
    """
    try:
        cpu = algolia_service.get_component_by_id(cpu_id)
        if not cpu:
            raise HTTPException(status_code=404, detail="CPU not found")
        
        suggestions = suggestion_service.suggest_compatible_motherboard(cpu)
        
        cpu_socket = cpu.get("specs", {}).get("socket") or cpu.get("socket", "unknown")
        
        return {
            "for_cpu": cpu.get("name"),
            "cpu_socket": cpu_socket,
            "suggestions": suggestions,
            "count": len(suggestions),
            "reasoning": f"Motherboards with {cpu_socket} socket"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/ram/{motherboard_id}")
async def suggest_ram(
    motherboard_id: str,
    budget: Optional[float] = Query(None, ge=0)
):
    """
    Suggest RAM compatible with motherboard memory type
    """
    try:
        motherboard = algolia_service.get_component_by_id(motherboard_id)
        if not motherboard:
            raise HTTPException(status_code=404, detail="Motherboard not found")
        
        suggestions = suggestion_service.suggest_ram(motherboard, budget=budget)
        
        mb_memory_type = motherboard.get("specs", {}).get("memory_type") or motherboard.get("memory_type", "unknown")
        
        return {
            "for_motherboard": motherboard.get("name"),
            "memory_type": mb_memory_type,
            "suggestions": suggestions,
            "count": len(suggestions),
            "reasoning": f"RAM compatible with {mb_memory_type}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/psu")
async def suggest_psu(
    total_power: int = Query(..., ge=0, description="Total system power in watts"),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Suggest PSU based on system power requirements
    Recommends PSU with 1.25x headroom
    """
    try:
        suggestions = suggestion_service.suggest_psu(total_power, limit=limit)
        recommended_wattage = int(total_power * 1.25)
        
        return {
            "total_power": total_power,
            "recommended_wattage": recommended_wattage,
            "suggestions": suggestions,
            "count": len(suggestions),
            "reasoning": f"PSU with ≥{recommended_wattage}W for {total_power}W system (25% headroom)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/storage")
async def suggest_storage(
    budget: Optional[float] = Query(None, ge=0),
    capacity_gb: Optional[int] = Query(None, ge=0),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Suggest storage options based on budget and capacity
    """
    try:
        suggestions = suggestion_service.suggest_storage(
            budget=budget,
            capacity_gb=capacity_gb,
            limit=limit
        )
        
        return {
            "budget": budget,
            "capacity_gb": capacity_gb,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")
