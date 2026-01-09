from fastapi import APIRouter, HTTPException
from typing import Dict
from app.services.compatibility_service import compatibility_service
from app.services.algolia_service import algolia_service
from app.models.component import BuildCompatibilityRequest, BuildCompatibilityResponse

router = APIRouter()

@router.post("/check-build", response_model=BuildCompatibilityResponse)
async def check_build_compatibility(build_request: BuildCompatibilityRequest):
    """
    Check compatibility of a complete PC build
    Validates CPU-motherboard socket, RAM type, PSU wattage, etc.
    """
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
        
        for component_type, component_id in component_mapping.items():
            if component_id:
                component = algolia_service.get_component_by_id(component_id)
                if component:
                    build_data[component_type] = component
        
        # Check compatibility
        result = compatibility_service.check_full_build(build_data)
        
        return BuildCompatibilityResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compatibility check error: {str(e)}")

@router.get("/check-pair/{component1_id}/{component2_id}")
async def check_component_pair(component1_id: str, component2_id: str):
    """
    Check compatibility between two specific components
    """
    try:
        comp1 = algolia_service.get_component_by_id(component1_id)
        comp2 = algolia_service.get_component_by_id(component2_id)
        
        if not comp1 or not comp2:
            raise HTTPException(status_code=404, detail="One or both components not found")
        
        # Determine component types
        type1 = comp1.get("type", "")
        type2 = comp2.get("type", "")
        
        compatible = True
        message = "Cannot determine compatibility between these component types"
        
        # Check based on types
        if ("CPU" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "CPU" in type2):
            cpu = comp1 if "CPU" in type1 else comp2
            mb = comp2 if "Motherboard" in type2 else comp1
            compatible, message = compatibility_service.check_cpu_motherboard(cpu, mb)
        
        elif ("Memory" in type1 and "Motherboard" in type2) or ("Motherboard" in type1 and "Memory" in type2):
            ram = comp1 if "Memory" in type1 else comp2
            mb = comp2 if "Motherboard" in type2 else comp1
            compatible, message = compatibility_service.check_ram_motherboard(ram, mb)
        
        elif ("GPU" in type1 or "Video" in type1) and "Motherboard" in type2:
            gpu = comp1
            mb = comp2
            compatible, message = compatibility_service.check_gpu_motherboard(gpu, mb)
        
        elif ("Motherboard" in type1) and ("GPU" in type2 or "Video" in type2):
            mb = comp1
            gpu = comp2
            compatible, message = compatibility_service.check_gpu_motherboard(gpu, mb)
        
        return {
            "component1": comp1.get("name"),
            "component2": comp2.get("name"),
            "compatible": compatible,
            "message": message
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking compatibility: {str(e)}")
