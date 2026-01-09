from typing import Dict, List, Tuple, Optional

class CompatibilityService:
    """Service for checking component compatibility"""
    
    @staticmethod
    def check_cpu_motherboard(cpu: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """
        Check if CPU socket matches motherboard socket
        
        Args:
            cpu: CPU component data
            motherboard: Motherboard component data
            
        Returns:
            Tuple of (is_compatible, message)
        """
        cpu_specs = cpu.get("specs", {})
        mb_specs = motherboard.get("specs", {})
        
        # Extract socket information
        cpu_socket = cpu_specs.get("socket") or cpu.get("socket")
        mb_socket = mb_specs.get("socket") or motherboard.get("socket")
        
        if not cpu_socket or not mb_socket:
            return False, "Missing socket information"
        
        if cpu_socket == mb_socket:
            return True, f"✓ Compatible: Both use {cpu_socket} socket"
        return False, f"✗ Incompatible: CPU uses {cpu_socket}, motherboard uses {mb_socket}"
    
    @staticmethod
    def check_ram_motherboard(ram: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """
        Check if RAM type matches motherboard memory type
        
        Args:
            ram: RAM component data
            motherboard: Motherboard component data
            
        Returns:
            Tuple of (is_compatible, message)
        """
        ram_specs = ram.get("specs", {})
        mb_specs = motherboard.get("specs", {})
        
        ram_type = ram_specs.get("type") or ram.get("type")
        mb_memory_type = mb_specs.get("memory_type") or motherboard.get("memory_type")
        
        if not ram_type or not mb_memory_type:
            return True, "⚠ Warning: Missing memory type information"
        
        # Extract DDR type (DDR4 or DDR5)
        ram_ddr = ram_type.upper()[: 4] if ram_type else None  # "DDR4" from "DDR4-3200"
        mb_ddr = mb_memory_type.upper()[:4] if mb_memory_type else None
        
        if ram_ddr and mb_ddr and ram_ddr == mb_ddr:
            return True, f"✓ Compatible: Both use {ram_ddr}"
        elif ram_ddr and mb_ddr:
            return False, f"✗ Incompatible: RAM is {ram_ddr}, motherboard supports {mb_ddr}"
        
        return True, "⚠ Warning: Cannot verify memory compatibility"
    
    @staticmethod
    def check_gpu_motherboard(gpu: Dict, motherboard: Dict) -> Tuple[bool, str]:
        """
        Check if motherboard has PCIe slot for GPU
        
        Args:
            gpu: GPU component data
            motherboard: Motherboard component data
            
        Returns:
            Tuple of (is_compatible, message)
        """
        # Modern motherboards all support GPUs
        # This is more of a warning system for older/incompatible combos
        mb_specs = motherboard.get("specs", {})
        
        form_factor = mb_specs.get("form_factor") or motherboard.get("form_factor", "")
        
        if form_factor and "Mini ITX" in form_factor:
            return True, "✓ Compatible (Note: Mini ITX has 1 PCIe slot)"
        
        return True, "✓ Compatible: Motherboard supports PCIe graphics cards"
    
    @staticmethod
    def check_gpu_psu(gpu: Dict, psu: Dict, cpu: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Check if PSU has enough wattage for GPU (and CPU if provided)
        
        Args:
            gpu: GPU component data
            psu: PSU component data
            cpu: Optional CPU component data
            
        Returns:
            Tuple of (is_compatible, message)
        """
        gpu_specs = gpu.get("specs", {})
        psu_specs = psu.get("specs", {})
        
        gpu_tdp = gpu_specs.get("tdp") or gpu.get("tdp", 200)  # Default estimate
        psu_wattage = psu_specs.get("wattage") or psu.get("wattage", 0)
        
        # Calculate total system power
        cpu_tdp = 0
        if cpu:
            cpu_specs = cpu.get("specs", {})
            cpu_tdp = cpu_specs.get("tdp") or cpu.get("tdp", 125)  # Default estimate
        
        # Total system power = GPU + CPU + 150W overhead (MB, RAM, storage, fans)
        total_power = gpu_tdp + cpu_tdp + 150
        
        # PSU should be 1.25x total power for headroom
        recommended_psu = int(total_power * 1.25)
        
        if psu_wattage >= recommended_psu:
            return True, f"✓ Compatible: {psu_wattage}W PSU sufficient for ~{total_power}W system"
        else:
            return False, f"✗ Insufficient: Need ≥{recommended_psu}W PSU, have {psu_wattage}W"
    
    @staticmethod
    def check_cpu_psu(cpu: Dict, psu: Dict) -> Tuple[bool, str]:
        """
        Check if PSU can power CPU
        
        Args:
            cpu: CPU component data
            psu: PSU component data
            
        Returns:
            Tuple of (is_compatible, message)
        """
        cpu_specs = cpu.get("specs", {})
        psu_specs = psu.get("specs", {})
        
        cpu_tdp = cpu_specs.get("tdp") or cpu.get("tdp", 125)
        psu_wattage = psu_specs.get("wattage") or psu.get("wattage", 0)
        
        # Basic system: CPU + 100W for other components
        min_required = cpu_tdp + 100
        
        if psu_wattage >= min_required:
            return True, f"✓ Compatible: PSU adequate for {cpu_tdp}W CPU"
        else:
            return False, f"✗ Insufficient: CPU needs ≥{min_required}W, PSU is {psu_wattage}W"
    
    @staticmethod
    def check_full_build(build: Dict) -> Dict:
        """
        Check all components in a build for compatibility
        
        Args:
            build: Dict with keys like 'cpu', 'gpu', 'motherboard', 'ram', 'psu'
            
        Returns:
            Dictionary with compatibility results
        """
        results = {
            "compatible": True,
            "checks": [],
            "warnings": [],
            "total_power": 0,
            "recommended_psu": 0,
        }
        
        cpu = build.get("cpu")
        motherboard = build.get("motherboard")
        gpu = build.get("gpu")
        psu = build.get("psu")
        ram = build.get("ram")
        
        # CPU-Motherboard
        if cpu and motherboard:
            compatible, msg = CompatibilityService.check_cpu_motherboard(cpu, motherboard)
            results["checks"].append({
                "check": "CPU-Motherboard Socket",
                "compatible": compatible,
                "message": msg,
                "severity": "error" if not compatible else "success"
            })
            if not compatible:
                results["compatible"] = False
        
        # RAM-Motherboard
        if ram and motherboard:
            compatible, msg = CompatibilityService.check_ram_motherboard(ram, motherboard)
            results["checks"].append({
                "check": "RAM-Motherboard Memory Type",
                "compatible": compatible,
                "message": msg,
                "severity": "error" if not compatible else "warning" if "Warning" in msg else "success"
            })
            if not compatible and "Warning" not in msg:
                results["compatible"] = False
            elif "Warning" in msg:
                results["warnings"].append(msg)
        
        # GPU-Motherboard
        if gpu and motherboard:
            compatible, msg = CompatibilityService.check_gpu_motherboard(gpu, motherboard)
            results["checks"].append({
                "check": "GPU-Motherboard PCIe",
                "compatible": compatible,
                "message": msg,
                "severity": "info" if compatible else "warning"
            })
            if "Note" in msg or "Warning" in msg:
                results["warnings"].append(msg)
        
        # PSU Power Checks
        if psu:
            # GPU-PSU
            if gpu:
                compatible, msg = CompatibilityService.check_gpu_psu(gpu, psu, cpu)
                results["checks"].append({
                    "check": "PSU Wattage (GPU)",
                    "compatible": compatible,
                    "message": msg,
                    "severity": "error" if not compatible else "success"
                })
                if not compatible:
                    results["compatible"] = False
            
            # CPU-PSU
            if cpu:
                compatible, msg = CompatibilityService.check_cpu_psu(cpu, psu)
                results["checks"].append({
                    "check": "PSU Wattage (CPU)",
                    "compatible": compatible,
                    "message": msg,
                    "severity": "error" if not compatible else "success"
                })
                if not compatible:
                    results["compatible"] = False
        
        # Calculate total power
        cpu_tdp = 0
        gpu_tdp = 0
        
        if cpu:
            cpu_specs = cpu.get("specs", {})
            cpu_tdp = cpu_specs.get("tdp") or cpu.get("tdp", 0)
        
        if gpu:
            gpu_specs = gpu.get("specs", {})
            gpu_tdp = gpu_specs.get("tdp") or gpu.get("tdp", 0)
        
        results["total_power"] = cpu_tdp + gpu_tdp + 150  # Add 150W overhead
        results["recommended_psu"] = int(results["total_power"] * 1.25)
        
        return results

# Create singleton instance
compatibility_service = CompatibilityService()
