from algoliasearch.search.client import SearchClientSync
from typing import List, Dict, Any, Optional, Union
import os
from dotenv import load_dotenv

load_dotenv()

class AlgoliaService:
    """Service for interacting with Algolia search"""
    
    def __init__(self):
        self.app_id = os.getenv("ALGOLIA_APP_ID")
        self.search_api_key = os.getenv("ALGOLIA_SEARCH_API_KEY")
        self.admin_api_key = os.getenv("ALGOLIA_ADMIN_API_KEY")
        
        if not all([self.app_id, self.search_api_key, self.admin_api_key]):
            raise ValueError("Missing Algolia credentials in environment variables")
        
        self.admin_client = SearchClientSync(self.app_id, self.admin_api_key)
        self.search_client = SearchClientSync(self.app_id, self.search_api_key)
        self.index_name = "pc_components"
    
    def _extract_search_result(self, response: Any) -> Any:
        """Extract actual search result from Algolia v4 API response wrapper"""
        if not response or not hasattr(response, 'results') or not response.results:
            return None
        
        result = response.results[0]
        return getattr(result, 'actual_instance', result)
    
    def _build_filters(self, filters: Optional[Dict[str, Any]] = None) -> tuple:
        """Build facet and numeric filters from filter dictionary"""
        facet_filters = []
        numeric_filters = []
        
        if not filters:
            return facet_filters, numeric_filters
        
        for key, value in filters.items():
            if key == "price_range" and isinstance(value, dict):
                min_price = value.get("min", 0)
                max_price = value.get("max")
                if min_price > 0:
                    numeric_filters.append(f"price>={min_price}")
                if max_price:
                    numeric_filters.append(f"price<={max_price}")
            elif key in ["type", "brand", "socket", "memory_type", "form_factor", "performance_tier"]:
                if isinstance(value, list):
                    facet_filters.append([f"{key}:{v}" for v in value])
                else:
                    facet_filters.append(f"{key}:{value}")
        
        return facet_filters, numeric_filters
    
    def search_components(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search components using Algolia
        
        Args:
            query: Search term (component name, brand, etc.)
            filters: Dictionary with filter criteria (type, brand, price_range, etc.)
            limit: Maximum results to return
            offset: Pagination offset
            
        Returns:
            Search results with hits, facets, and metadata
        """
        facet_filters, numeric_filters = self._build_filters(filters)
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": query,
                        "hitsPerPage": limit,
                        "page": offset // limit,
                        "facetFilters": facet_filters,
                        "numericFilters": numeric_filters,
                        "attributesToRetrieve": ["*"],
                        "attributesToHighlight": ["name", "brand"],
                        "analytics": True,
                    }]
                }
            )
            
            result = self._extract_search_result(response)
            if not result:
                return {"hits": [], "nbHits": 0}
            
            return {
                "hits": getattr(result, 'hits', []),
                "nbHits": getattr(result, 'nb_hits', 0),
                "page": getattr(result, 'page', 0),
                "nbPages": getattr(result, 'nb_pages', 0),
                "hitsPerPage": getattr(result, 'hits_per_page', limit),
                "processingTimeMS": getattr(result, 'processing_time_ms', 0),
                "facets": getattr(result, 'facets', {})
            }
        except Exception as e:
            print(f"Algolia search error: {e}")
            return {"hits": [], "nbHits": 0, "error": str(e)}
    
    def search_by_type(
        self,
        component_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50
    ) -> List[Any]:
        """
        Search components by type (CPU, GPU, etc.)
        
        Args:
            component_type: Component type to filter by (CPU, GPU, Motherboard, etc.)
            filters: Additional filters (socket, brand, performance_tier, price_range)
            limit: Maximum results
            
        Returns:
            List of matching components
        """
        # Start with type filter
        type_filters = {"type": component_type}
        if filters:
            type_filters.update(filters)
        
        facet_filters, numeric_filters = self._build_filters(type_filters)
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "facetFilters": facet_filters,
                        "numericFilters": numeric_filters,
                        "hitsPerPage": limit,
                        "analytics": True
                    }]
                }
            )
            
            result = self._extract_search_result(response)
            return getattr(result, 'hits', []) if result else []
        except Exception as e:
            print(f"Algolia search by type error: {e}")
            return []
    
    def get_component_by_id(self, component_id: str) -> Optional[Any]:
        """
        Get a single component by ID
        
        Args:
            component_id: Unique component identifier (objectID)
            
        Returns:
            Component data or None if not found
        """
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "filters": f"objectID:{component_id}",
                        "hitsPerPage": 1
                    }]
                }
            )
            
            result = self._extract_search_result(response)
            if result:
                hits = getattr(result, 'hits', [])
                return hits[0] if hits else None
            return None
        except Exception as e:
            print(f"Error fetching component by ID: {e}")
            return None
    
    def get_facets(self, component_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available facet values for filtering UI dropdowns
        
        Args:
            component_type: Optional type filter to get facets for specific component type
            
        Returns:
            Dictionary of facet values (brand, socket, performance_tier, etc.)
        """
        facet_list = ["brand", "type", "performance_tier", "socket", "memory_type", "form_factor"]
        facet_filters = [f"type:{component_type}"] if component_type else []
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "facets": facet_list,
                        "hitsPerPage": 0,
                        "facetFilters": facet_filters
                    }]
                }
            )
            
            result = self._extract_search_result(response)
            return getattr(result, 'facets', {}) if result else {}
        except Exception as e:
            print(f"Error fetching facets: {e}")
            return {}
    
    def partial_update_components(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Partially update components (e.g., add reviews)
        
        Args:
            updates: List of objects with objectID and fields to update
            
        Returns:
            Success status and task ID
        """
        if not updates:
            return {"success": False, "error": "No updates provided"}
        
        try:
            response = self.admin_client.partial_update_objects(
                index_name=self.index_name,
                objects=updates,
                create_if_not_exists=False
            )
            
            task_id = getattr(response, 'task_id', None)
            if not task_id and isinstance(response, dict):
                task_id = response.get("taskID")
            
            return {"success": True, "taskID": task_id, "count": len(updates)}
        except Exception as e:
            print(f"Error updating components: {e}")
            return {"success": False, "error": str(e)}

    def index_components(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Index components to Algolia (admin operation)
        
        Args:
            components: List of component dictionaries to index
            
        Returns:
            Indexing response with success status and task ID
        """
        if not components:
            return {"success": False, "error": "No components to index"}
        
        # Ensure each component has objectID
        for component in components:
            if "objectID" not in component:
                component["objectID"] = component.get("id", f"auto_{hash(str(component))}")
        
        try:
            response = self.admin_client.save_objects(
                index_name=self.index_name,
                objects=components
            )
            
            # Handle different response types
            if isinstance(response, list):
                return {"success": True, "count": len(components), "batches": len(response)}
            
            task_id = getattr(response, 'task_id', None)
            if not task_id and isinstance(response, dict):
                task_id = response.get("taskID")
            
            return {"success": True, "taskID": task_id, "count": len(components)}
        except Exception as e:
            print(f"Error indexing components: {e}")
            return {"success": False, "error": str(e)}
    
    def clear_index(self) -> Dict[str, Any]:
        """
        Clear all objects from the index (admin operation)
        
        Returns:
            Clear operation response with success status
        """
        try:
            response = self.admin_client.clear_objects(index_name=self.index_name)
            
            task_id = getattr(response, 'task_id', None)
            if not task_id and isinstance(response, dict):
                task_id = response.get("taskID")
            
            return {"success": True, "taskID": task_id}
        except Exception as e:
            print(f"Error clearing index: {e}")
            return {"success": False, "error": str(e)}
    
    def configure_index_settings(self) -> Dict[str, Any]:
        """
        Configure Algolia index settings for optimal PC component search
        
        Returns:
            Settings update response with success status
        """
        settings = {
            "searchableAttributes": [
                "name",
                "brand",
                "type",
                "unordered(specs.socket)",
                "unordered(specs.memory_type)",
            ],
            "attributesForFaceting": [
                "type",
                "brand",
                "searchable(socket)",
                "searchable(memory_type)",
                "form_factor",
                "performance_tier",
            ],
            "customRanking": [
                "desc(performance_tier)",
                "desc(release_year)",
                "asc(price)",
            ],
            "attributesToHighlight": [
                "name",
                "brand",
            ],
            "attributesToSnippet": [
                "name:20",
            ],
            "hitsPerPage": 20,
            "maxValuesPerFacet": 100,
            "typoTolerance": True,
            "minWordSizefor1Typo": 4,
            "minWordSizefor2Typos": 8,
            "allowTyposOnNumericTokens": False,
        }
        
        try:
            response = self.admin_client.set_settings(
                index_name=self.index_name,
                index_settings=settings
            )
            
            task_id = getattr(response, 'task_id', None)
            if not task_id and isinstance(response, dict):
                task_id = response.get("taskID")
            
            return {"success": True, "taskID": task_id}
        except Exception as e:
            print(f"Error configuring index settings: {e}")
            return {"success": False, "error": str(e)}


# Create singleton instance
algolia_service = AlgoliaService()
