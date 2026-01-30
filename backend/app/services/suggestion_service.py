from app.services.algolia_service import algolia_service
from typing import List, Dict, Optional
import re
from datetime import datetime

# ==================== MULTI-FACTOR SCORING SYSTEM ====================

class ComponentScorer:
    """
    Multi-factor scoring system for intelligent component recommendations.
    Considers: tier matching, value, popularity, power efficiency, and future-proofing.
    """
    
    # Scoring weights (should sum to 1.0)
    WEIGHTS = {
        'tier_match': 0.25,      # Performance tier compatibility
        'value_score': 0.25,     # Price-to-performance ratio
        'popularity': 0.20,      # Community preference / reviews
        'power_efficiency': 0.15, # Performance per watt
        'future_proof': 0.15     # Longevity, features, VRAM, etc.
    }
    
    # Price thresholds for tier classification
    TIER_THRESHOLDS = {
        'CPU': {'high': 400, 'mid': 200},
        'GPU': {'high': 800, 'mid': 400},
        'Motherboard': {'high': 300, 'mid': 150},
        'Memory': {'high': 150, 'mid': 80},
        'Power Supply': {'high': 150, 'mid': 80},
        'Internal Hard Drive': {'high': 200, 'mid': 100}
    }
    
    @classmethod
    def calculate_tier_match_score(cls, component: Dict, target_tier: str) -> float:
        """
        Score based on how well component tier matches target tier.
        Perfect match = 100, adjacent tier = 70, opposite = 40
        """
        comp_tier = component.get('performance_tier', 'mid-range')
        
        tier_order = ['budget', 'mid-range', 'high-end']
        try:
            comp_idx = tier_order.index(comp_tier)
            target_idx = tier_order.index(target_tier)
            diff = abs(comp_idx - target_idx)
            
            if diff == 0:
                return 100
            elif diff == 1:
                return 70
            else:
                return 40
        except ValueError:
            return 50  # Unknown tier
    
    @classmethod
    def calculate_value_score(cls, component: Dict, component_type: str) -> float:
        """
        Calculate price-to-performance value score.
        Higher score = better value for money.
        """
        price = component.get('price', 0)
        if price <= 0:
            return 50  # Unknown price
        
        # Get tier thresholds for this component type
        thresholds = cls.TIER_THRESHOLDS.get(component_type, {'high': 500, 'mid': 200})
        tier = component.get('performance_tier', 'mid-range')
        
        # Expected price ranges by tier
        expected_ranges = {
            'budget': (0, thresholds['mid']),
            'mid-range': (thresholds['mid'], thresholds['high']),
            'high-end': (thresholds['high'], thresholds['high'] * 2)
        }
        
        expected_min, expected_max = expected_ranges.get(tier, (0, 500))
        expected_mid = (expected_min + expected_max) / 2
        
        # Score: 100 if at/below expected, decreasing as price exceeds expected
        if price <= expected_mid:
            return min(100, 70 + (30 * (1 - price / max(expected_mid, 1))))
        else:
            overage_ratio = (price - expected_mid) / max(expected_mid, 1)
            return max(30, 100 - (overage_ratio * 50))
    
    @classmethod
    def calculate_popularity_score(cls, component: Dict) -> float:
        """
        Score based on reviews and ratings.
        """
        rating = component.get('rating', {})
        if isinstance(rating, dict):
            avg_rating = rating.get('average', 0)
            review_count = rating.get('count', 0)
        else:
            avg_rating = 0
            review_count = 0
        
        # Also check legacy fields
        if not avg_rating:
            avg_rating = component.get('average_rating', 0)
        if not review_count:
            review_count = component.get('review_count', 0)
        
        # Base score from rating (0-5 stars -> 0-100)
        rating_score = (avg_rating / 5) * 100 if avg_rating else 50
        
        # Bonus for more reviews (up to 20 points)
        review_bonus = min(20, review_count / 50 * 20)
        
        return min(100, rating_score * 0.8 + review_bonus)
    
    @classmethod
    def calculate_power_efficiency_score(cls, component: Dict) -> float:
        """
        Score based on TDP and performance tier.
        Lower TDP for same tier = better.
        """
        specs = component.get('specs', {})
        tdp = specs.get('tdp') or component.get('tdp', 0)
        tier = component.get('performance_tier', 'mid-range')
        
        if not tdp:
            return 50  # Unknown TDP
        
        # Expected TDP ranges by tier
        expected_tdp = {
            'budget': (35, 65),
            'mid-range': (65, 125),
            'high-end': (125, 250)
        }
        
        expected_min, expected_max = expected_tdp.get(tier, (65, 125))
        
        if tdp <= expected_min:
            return 100  # Very efficient
        elif tdp <= expected_max:
            # Scale from 100 to 60 within expected range
            ratio = (tdp - expected_min) / (expected_max - expected_min)
            return 100 - (ratio * 40)
        else:
            # Above expected, score decreases
            overage = (tdp - expected_max) / expected_max
            return max(20, 60 - (overage * 40))
    
    @classmethod
    def calculate_future_proof_score(cls, component: Dict, component_type: str) -> float:
        """
        Score based on features that affect longevity.
        """
        specs = component.get('specs', {})
        name = component.get('name', '').lower()
        score = 50  # Base score
        
        if component_type == 'GPU':
            # VRAM is key for future-proofing
            vram_match = re.search(r'(\d+)\s*gb', name)
            if vram_match:
                vram = int(vram_match.group(1))
                if vram >= 16:
                    score += 30
                elif vram >= 12:
                    score += 20
                elif vram >= 8:
                    score += 10
            
            # Newer architectures
            if any(x in name for x in ['4090', '4080', '4070', '7900', '7800']):
                score += 20
            elif any(x in name for x in ['3080', '3070', '6800', '6900']):
                score += 10
                
        elif component_type == 'CPU':
            # Core count
            cores = specs.get('core_count', 0)
            if cores >= 16:
                score += 25
            elif cores >= 12:
                score += 20
            elif cores >= 8:
                score += 15
            elif cores >= 6:
                score += 10
            
            # Modern platforms (AM5, LGA1700)
            socket = specs.get('socket', '') or component.get('socket', '')
            if socket in ['AM5', 'LGA1700']:
                score += 15
            elif socket in ['AM4', 'LGA1200']:
                score += 5
                
        elif component_type == 'Motherboard':
            # DDR5 support
            mem_type = specs.get('memory_type', '')
            if 'DDR5' in mem_type.upper():
                score += 20
            
            # PCIe 5.0
            if 'pcie 5' in name or 'pcie5' in name:
                score += 15
                
        elif component_type == 'Memory':
            # DDR5 is more future-proof
            if 'ddr5' in name:
                score += 25
            
            # Higher speeds
            speed_match = re.search(r'(\d{4,5})', name)
            if speed_match:
                speed = int(speed_match.group(1))
                if speed >= 6000:
                    score += 15
                elif speed >= 5200:
                    score += 10
        
        return min(100, score)
    
    @classmethod
    def calculate_total_score(cls, component: Dict, component_type: str, target_tier: str = 'mid-range') -> Dict:
        """
        Calculate total recommendation score with breakdown.
        """
        scores = {
            'tier_match': cls.calculate_tier_match_score(component, target_tier),
            'value_score': cls.calculate_value_score(component, component_type),
            'popularity': cls.calculate_popularity_score(component),
            'power_efficiency': cls.calculate_power_efficiency_score(component),
            'future_proof': cls.calculate_future_proof_score(component, component_type)
        }
        
        # Weighted total
        total = sum(scores[key] * cls.WEIGHTS[key] for key in scores)
        
        return {
            'total': round(total, 1),
            'breakdown': {k: round(v, 1) for k, v in scores.items()}
        }


class SuggestionService:
    """Service for suggesting compatible components with intelligent scoring"""
    
    @staticmethod
    def suggest_cpus(
        budget: Optional[float] = None,
        use_case: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Suggest CPUs based on budget, use case, and multi-factor scoring.
        
        Args:
            budget: Maximum budget
            use_case: Use case (gaming, streaming, workstation)
            limit: Maximum suggestions
            
        Returns:
            List of suggested CPUs with recommendation scores
        """
        filters = {}
        
        if budget:
            filters["price_range"] = {"min": 0, "max": budget}
        
        results = algolia_service.search_by_type("CPU", filters=filters, limit=limit * 3)
        
        # Determine target tier based on budget and use case
        target_tier = 'mid-range'
        if budget:
            if budget >= 400:
                target_tier = 'high-end'
            elif budget < 200:
                target_tier = 'budget'
        
        if use_case == 'workstation':
            target_tier = 'high-end'  # Workstations need power
        
        # Score and sort results
        scored_results = []
        for cpu in results:
            scores = ComponentScorer.calculate_total_score(cpu, 'CPU', target_tier)
            cpu['recommendation_score'] = scores['total']
            cpu['score_breakdown'] = scores['breakdown']
            scored_results.append(cpu)
        
        # Sort by recommendation score
        scored_results.sort(key=lambda x: x.get('recommendation_score', 0), reverse=True)
        
        return scored_results[:limit]
    
    @staticmethod
    def suggest_compatible_gpu(
        cpu: Dict,
        budget: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Suggest GPUs that pair well with given CPU using multi-factor scoring.
        Avoids bottlenecking by matching performance tiers.
        
        Args:
            cpu: CPU component data
            budget: Maximum budget
            limit: Maximum suggestions
            
        Returns:
            List of suggested GPUs with recommendation scores
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
        target_tier = suggested_tiers[0]  # Primary target
        
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
        
        # Score results
        scored_results = []
        for gpu in matched_results:
            scores = ComponentScorer.calculate_total_score(gpu, 'GPU', target_tier)
            gpu['recommendation_score'] = scores['total']
            gpu['score_breakdown'] = scores['breakdown']
            scored_results.append(gpu)
        
        # Sort by recommendation score
        scored_results.sort(key=lambda x: x.get('recommendation_score', 0), reverse=True)
        
        return scored_results[:limit]
    
    @staticmethod
    def suggest_compatible_motherboard(cpu: Dict, limit: int = 5) -> List[Dict]:
        """
        Suggest motherboards compatible with CPU socket using multi-factor scoring.
        
        Args:
            cpu: CPU component data
            limit: Maximum suggestions
            
        Returns:
            List of suggested motherboards with recommendation scores
        """
        cpu_specs = cpu.get("specs", {})
        cpu_socket = cpu_specs.get("socket") or cpu.get("socket")
        cpu_tier = cpu_specs.get("performance_tier") or cpu.get("performance_tier", "mid-range")
        
        if not cpu_socket:
            return []
        
        filters = {"socket": cpu_socket}
        results = algolia_service.search_by_type("Motherboard", filters=filters, limit=limit * 3)
        
        # Score results
        scored_results = []
        for mb in results:
            scores = ComponentScorer.calculate_total_score(mb, 'Motherboard', cpu_tier)
            mb['recommendation_score'] = scores['total']
            mb['score_breakdown'] = scores['breakdown']
            scored_results.append(mb)
        
        # Sort by recommendation score
        scored_results.sort(key=lambda x: x.get('recommendation_score', 0), reverse=True)
        
        return scored_results[:limit]
    
    @staticmethod
    def suggest_ram(
        motherboard: Dict,
        budget: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Suggest RAM compatible with motherboard using multi-factor scoring.
        
        Args:
            motherboard: Motherboard component data
            budget: Maximum budget
            limit: Maximum suggestions
            
        Returns:
            List of suggested RAM with recommendation scores
        """
        mb_specs = motherboard.get("specs", {})
        memory_type = mb_specs.get("memory_type") or motherboard.get("memory_type", "DDR5")
        mb_tier = motherboard.get("performance_tier", "mid-range")
        
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
            if ddr_type.upper() in (ram.get("name", "") + str(ram.get("type", ""))).upper()
        ]
        
        # Score results
        scored_results = []
        for ram in matched:
            scores = ComponentScorer.calculate_total_score(ram, 'Memory', mb_tier)
            ram['recommendation_score'] = scores['total']
            ram['score_breakdown'] = scores['breakdown']
            scored_results.append(ram)
        
        # Sort by recommendation score
        scored_results.sort(key=lambda x: x.get('recommendation_score', 0), reverse=True)
        
        return scored_results[:limit]
    
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
