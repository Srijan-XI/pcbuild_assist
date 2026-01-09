from app.services.algolia_service import algolia_service
from typing import List, Dict, Optional

class SuggestionService:
    """Service for suggesting compatible components"""
    
    @staticmethod
    def suggest_cpus(
        budget: Optional[float] = None,
        use_case: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Suggest CPUs based on budget and use case
        
        Args:
            budget: Maximum budget
            use_case: Use case (gaming, streaming, workstation)
            limit: Maximum suggestions
            
        Returns:
            List of suggested CPUs
        """
        filters = {}
        
        if budget:
            filters["price_range"] = {"min": 0, "max": budget}
        
        results = algolia_service.search_by_type("CPU", filters=filters, limit=limit)
        
        # Sort by performance tier and price
        results.sort(key=lambda x: (
            {"high-end": 0, "mid-range": 1, "budget": 2}.get(x.get("performance_tier",""), 3),
            x.get("price", 999999)
        ))
        
        return results[:limit]
    
    @staticmethod
    def suggest_compatible_gpu(
        cpu: Dict,
        budget: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Suggest GPUs that pair well with given CPU
        Avoid bottlenecking by matching performance tiers
        
        Args:
            cpu: CPU component data
            budget: Maximum budget
            limit: Maximum suggestions
            
        Returns:
            List of suggested GPUs
        """
        cpu_specs = cpu.get("specs", {})
        cpu_tier = cpu_specs.get("performance_tier") or cpu.get("performance_tier", "mid-range")
        
        # Map CPU tier to appropriate GPU tier
        tier_mapping = {
            "high-end": ["high-end", "mid-range"],
            "mid-range": ["mid-range", "high-end"],
            "budget": ["budget", "mid-range"]
        }
        
        suggested_tiers = tier_mapping.get(cpu_tier, ["mid-range"])
        
        filters = {}
        if budget:
            filters["price_range"] = {"min": 0, "max": budget}
        
        # Search GPUs
        all_results = algolia_service.search_by_type("GPU", filters=filters, limit=50)
        
        # Filter by performance tier
        matched_results = [
            gpu for gpu in all_results
            if gpu.get("performance_tier") in suggested_tiers
        ]
        
        # Sort by price
        matched_results.sort(key=lambda x: x.get("price", 999999))
        
        return matched_results[:limit]
    
    @staticmethod
    def suggest_compatible_motherboard(cpu: Dict, limit: int = 5) -> List[Dict]:
        """
        Suggest motherboards compatible with CPU socket
        
        Args:
            cpu: CPU component data
            limit: Maximum suggestions
            
        Returns:
            List of suggested motherboards
        """
        cpu_specs = cpu.get("specs", {})
        cpu_socket = cpu_specs.get("socket") or cpu.get("socket")
        
        if not cpu_socket:
            return []
        
        filters = {"socket": cpu_socket}
        results = algolia_service.search_by_type("Motherboard", filters=filters, limit=limit * 2)
        
        # Sort by price
        results.sort(key=lambda x: x.get("price", 999999))
        
        return results[:limit]
    
    @staticmethod
    def suggest_ram(
        motherboard: Dict,
        budget: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Suggest RAM compatible with motherboard
        
        Args:
            motherboard: Motherboard component data
            budget: Maximum budget
            limit: Maximum suggestions
            
        Returns:
            List of suggested RAM
        """
        mb_specs = motherboard.get("specs", {})
        memory_type = mb_specs.get("memory_type") or motherboard.get("memory_type", "DDR5")
        
        # Extract DDR type (DDR4 or DDR5)
        ddr_type = memory_type[:4] if memory_type else "DDR5"
        
        filters = {}
        if budget:
            filters["price_range"] = {"min": 0, "max": budget}
        
        # Search Memory
        results = algolia_service.search_by_type("Memory", filters=filters, limit=50)
        
        # Filter by DDR type
        matched = [
            ram for ram in results
            if ddr_type.upper() in (ram.get("name", "") + ram.get("type", "")).upper()
        ]
        
        # Sort by capacity and price
        matched.sort(key=lambda x: (
            -int(''.join(filter(str.isdigit, x.get("name", "0")[:3])) or 0),  # Capacity (higher first)
            x.get("price", 999999)  # Price (lower first)
        ))
        
        return matched[:limit]
    
    @staticmethod
    def suggest_psu(total_power: int, limit: int = 5) -> List[Dict]:
        """
        Suggest PSU with 1.25x headroom over total power
        
        Args:
            total_power: Total system power consumption in watts
            limit: Maximum suggestions
            
        Returns:
            List of suggested PSUs
        """
        recommended_wattage = int(total_power * 1.25)
        
        # Search all PSUs
        results = algolia_service.search_by_type("Power Supply", limit=100)
        
        # Extract wattage from name (e.g., "Corsair RM1000x" -> 1000)
        def extract_wattage(psu: Dict) -> int:
            name = psu.get("name", "")
            # Look for wattage in name
            import re
            match = re.search(r'(\d{3,4})[Ww]?', name)
            if match:
                return int(match.group(1))
            
            # Check specs
            specs = psu.get("specs", {})
            return specs.get("wattage", 0)
        
        # Filter PSUs with adequate wattage
        suitable_psus = [
            {**psu, "wattage": extract_wattage(psu)}
            for psu in results
            if extract_wattage(psu) >= recommended_wattage
        ]
        
        # Sort by wattage (closest to recommended) then price
        suitable_psus.sort(key=lambda x: (
            abs(x["wattage"] - recommended_wattage),
            x.get("price", 999999)
        ))
        
        return suitable_psus[:limit]
    
    @staticmethod
    def suggest_storage(
        budget: Optional[float] = None,
        capacity_gb: Optional[int] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Suggest storage options
        
        Args:
            budget: Maximum budget
            capacity_gb: Desired capacity in GB
            limit: Maximum suggestions
            
        Returns:
            List of suggested storage devices
        """
        filters = {}
        if budget:
            filters["price_range"] = {"min": 0, "max": budget}
        
        # Search internal hard drives and SSDs
        results = algolia_service.search_by_type("Internal Hard Drive", filters=filters, limit=limit * 2)
        
        # Prioritize SSDs
        results.sort(key=lambda x: (
            0 if "SSD" in x.get("name", "") or "NVMe" in x.get("name", "") else 1,
            x.get("price", 999999)
        ))
        
        return results[:limit]

# Create singleton instance
suggestion_service = SuggestionService()
