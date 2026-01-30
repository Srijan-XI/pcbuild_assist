from fastapi import APIRouter, Request
from typing import Dict, List
import time

from app.services.compatibility_service import compatibility_service
from app.services.algolia_service import algolia_service
from app.models.component import BuildCompatibilityRequest, BuildCompatibilityResponse
from app.core.exceptions import NotFoundException, ValidationException, AlgoliaException
from app.core.responses import success_response
from app.core.cache import cache
from app.core.logging import get_logger, get_request_id
from app.core.rate_limit import limiter

router = APIRouter()
logger = get_logger(__name__)


@router.post("/check-build")
@limiter.limit("30/minute")
async def check_build_compatibility(
    request: Request,
    build_request: BuildCompatibilityRequest
):
    """
    Check compatibility of a complete PC build.
    
    Validates:
    - CPU-motherboard socket compatibility
    - RAM type and speed compatibility
    - PSU wattage requirements
    - Physical clearances
    
    **Rate Limit:** 30 requests/minute
    """
    start_time = time.perf_counter()
    
    try:
        # Fetch actual component data from Algolia
        build_data = {}
        
        component_mapping = {
            "cpu": build_request.cpu_id,
            "motherboard": build_request.motherboard_id,
            "gpu": build_request.gpu_id,
            "ram": build_request.ram_id,
            "psu": build_request.psu_id,
        }
        
        # Track which components were requested vs found
        components_requested = []
        components_found = []
        
        for component_type, component_id in component_mapping.items():
            if component_id:
                components_requested.append(component_type)
                component = algolia_service.get_component_by_id(component_id)
                if component:
                    build_data[component_type] = component
                    components_found.append(component_type)
        
        logger.info("Checking build compatibility", data={
            "components_requested": components_requested,
            "components_found": components_found
        })
        
        # Check compatibility
        result = compatibility_service.check_full_build(build_data)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "is_compatible": result.get("is_compatible", False),
                "overall_score": result.get("overall_score", 0),
                "issues": result.get("issues", []),
                "warnings": result.get("warnings", []),
                "recommendations": result.get("recommendations", []),
                "power_analysis": result.get("power_analysis", {}),
                "components_analyzed": components_found
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    
    except Exception as e:
        logger.error(f"Build compatibility check failed: {str(e)}")
        raise AlgoliaException(operation="check_build", message=str(e))


@router.get("/check-pair/{component1_id}/{component2_id}")
@limiter.limit("60/minute")
async def check_component_pair(
    request: Request,
    component1_id: str,
    component2_id: str
):
    """
    Check compatibility between two specific components.
    
    Supports checking:
    - CPU ↔ Motherboard (socket)
    - RAM ↔ Motherboard (DDR type)
    - GPU ↔ Motherboard (PCIe)
    
    **Rate Limit:** 60 requests/minute
    """
    start_time = time.perf_counter()
    
    # Check cache first
    cache_key = f"pair:{min(component1_id, component2_id)}:{max(component1_id, component2_id)}"
    cached_result = cache.get("compatibility", cache_key)
    if cached_result:
        return success_response(
            data=cached_result,
            request_id=get_request_id(),
            processing_time_ms=0
        )
    
    try:
        comp1 = algolia_service.get_component_by_id(component1_id)
        comp2 = algolia_service.get_component_by_id(component2_id)
        
        if not comp1:
            raise NotFoundException(resource="Component", identifier=component1_id)
        if not comp2:
            raise NotFoundException(resource="Component", identifier=component2_id)
        
        # Determine component types
        type1 = comp1.get("type", "")
        type2 = comp2.get("type", "")
        
        compatible = True
        message = "Cannot determine compatibility between these component types"
        compatibility_type = "unknown"
        
        # Check based on types
        if ("CPU" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "CPU" in type2):
            cpu = comp1 if "CPU" in type1 else comp2
            mb = comp2 if "Motherboard" in type2 else comp1
            compatible, message = compatibility_service.check_cpu_motherboard(cpu, mb)
            compatibility_type = "cpu_motherboard_socket"
        
        elif ("Memory" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "Memory" in type2):
            ram = comp1 if "Memory" in type1 else comp2
            mb = comp2 if "Motherboard" in type2 else comp1
            compatible, message = compatibility_service.check_ram_motherboard(ram, mb)
            compatibility_type = "ram_motherboard_ddr"
        
        elif ("GPU" in type1 or "Video" in type1) and "Motherboard" in type2:
            gpu = comp1
            mb = comp2
            compatible, message = compatibility_service.check_gpu_motherboard(gpu, mb)
            compatibility_type = "gpu_motherboard_pcie"
        
        elif ("Motherboard" in type1) and ("GPU" in type2 or "Video" in type2):
            mb = comp1
            gpu = comp2
            compatible, message = compatibility_service.check_gpu_motherboard(gpu, mb)
            compatibility_type = "gpu_motherboard_pcie"
        
        result = {
            "component1": {
                "id": component1_id,
                "name": comp1.get("name"),
                "type": type1
            },
            "component2": {
                "id": component2_id,
                "name": comp2.get("name"),
                "type": type2
            },
            "compatible": compatible,
            "compatibility_type": compatibility_type,
            "message": message
        }
        
        # Cache the result
        cache.set("compatibility", cache_key, result)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        logger.info("Pair compatibility check completed", data={
            "type1": type1,
            "type2": type2,
            "compatible": compatible
        })
        
        return success_response(
            data=result,
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
    
    except NotFoundException:
        raise
    except Exception as e:
        logger.error(f"Pair compatibility check failed: {str(e)}")
        raise AlgoliaException(operation="check_pair", message=str(e))


@router.post("/batch-check")
@limiter.limit("10/minute")
async def batch_check_compatibility(
    request: Request,
    component_ids: List[str]
):
    """
    Check compatibility between multiple components at once.
    
    Performs pairwise compatibility checks for all provided components.
    Useful for validating partial builds.
    
    **Rate Limit:** 10 requests/minute (expensive operation)
    """
    start_time = time.perf_counter()
    
    if len(component_ids) < 2:
        raise ValidationException(
            message="At least 2 component IDs are required",
            field="component_ids"
        )
    
    if len(component_ids) > 10:
        raise ValidationException(
            message="Maximum 10 components per batch check",
            field="component_ids"
        )
    
    try:
        # Fetch all components
        components = {}
        for comp_id in component_ids:
            comp = algolia_service.get_component_by_id(comp_id)
            if comp:
                components[comp_id] = comp
        
        if len(components) < 2:
            raise ValidationException(
                message="Could not find enough valid components",
                field="component_ids"
            )
        
        # Perform pairwise checks
        checks = []
        issues = []
        all_compatible = True
        
        comp_list = list(components.items())
        for i in range(len(comp_list)):
            for j in range(i + 1, len(comp_list)):
                id1, comp1 = comp_list[i]
                id2, comp2 = comp_list[j]
                
                type1 = comp1.get("type", "")
                type2 = comp2.get("type", "")
                
                # Only check relevant pairs
                relevant_pairs = [
                    ("CPU", "Motherboard"),
                    ("Memory", "Motherboard"),
                    ("GPU", "Motherboard"),
                    ("Video Card", "Motherboard")
                ]
                
                is_relevant = False
                for t1, t2 in relevant_pairs:
                    if (t1 in type1 and t2 in type2) or (t1 in type2 and t2 in type1):
                        is_relevant = True
                        break
                
                if not is_relevant:
                    continue
                
                # Check compatibility
                compatible = True
                message = "Compatible"
                
                if ("CPU" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "CPU" in type2):
                    cpu = comp1 if "CPU" in type1 else comp2
                    mb = comp2 if "Motherboard" in type2 else comp1
                    compatible, message = compatibility_service.check_cpu_motherboard(cpu, mb)
                elif ("Memory" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "Memory" in type2):
                    ram = comp1 if "Memory" in type1 else comp2
                    mb = comp2 if "Motherboard" in type2 else comp1
                    compatible, message = compatibility_service.check_ram_motherboard(ram, mb)
                elif ("GPU" in type1 or "Video" in type1) or ("GPU" in type2 or "Video" in type2):
                    if "Motherboard" in type1:
                        mb, gpu = comp1, comp2
                    else:
                        gpu, mb = comp1, comp2
                    compatible, message = compatibility_service.check_gpu_motherboard(gpu, mb)
                
                check_result = {
                    "component1": {"id": id1, "name": comp1.get("name"), "type": type1},
                    "component2": {"id": id2, "name": comp2.get("name"), "type": type2},
                    "compatible": compatible,
                    "message": message
                }
                checks.append(check_result)
                
                if not compatible:
                    all_compatible = False
                    issues.append(message)
        
        process_time = int((time.perf_counter() - start_time) * 1000)
        
        return success_response(
            data={
                "all_compatible": all_compatible,
                "components_checked": len(components),
                "pairs_checked": len(checks),
                "checks": checks,
                "issues": issues
            },
            request_id=get_request_id(),
            processing_time_ms=process_time
        )
        
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Batch compatibility check failed: {str(e)}")
        raise AlgoliaException(operation="batch_check", message=str(e))

