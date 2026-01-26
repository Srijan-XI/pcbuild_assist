from algoliasearch.search.client import SearchClientSync
from typing import List, Dict, Any, Optional
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
        
        # Client for admin operations (indexing) - v4 API
        self.admin_client = SearchClientSync(self.app_id, self.admin_api_key)
        self.index_name = "pc_components"
        
        # Client for search operations
        self.search_client = SearchClientSync(self.app_id, self.search_api_key)
        
        # Initialize index references - Removed in v4, use client methods with index_name
        # self.index and self.search_index are not needed

    
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
            filters: Dictionary with filter criteria
            limit: Maximum results to return
            offset: Pagination offset
            
        Returns:
            Search results with hits, facets, and metadata
        """
        search_params = {
            "query": query,
            "hitsPerPage": limit,
            "page": offset // limit,
            "analytics": True,  # Track searches for insights
            "attributesToRetrieve": ["*"],
            "attributesToHighlight": ["name", "brand"],
        }
        
        # Build facet filters
        if filters:
            facet_filters = []
            numeric_filters = []
            
            for key, value in filters.items():
                if key == "price_range" and isinstance(value, dict):
                    # Handle price range
                    min_price = value.get("min", 0)
                    max_price = value.get("max")
                    if max_price:
                        numeric_filters.append(f"price>={min_price}")
                        numeric_filters.append(f"price<={max_price}")
                elif key in ["type", "brand", "socket", "memory_type", "form_factor", "performance_tier"]:
                    # Exact match filters
                    if isinstance(value, list):
                        facet_filters.append([f"{key}:{v}" for v in value])
                    else:
                        facet_filters.append(f"{key}:{value}")
            
            if facet_filters:
                search_params["facetFilters"] = facet_filters
            if numeric_filters:
                search_params["numericFilters"] = numeric_filters
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": query,
                        "hitsPerPage": limit,
                        "page": offset // limit,
                        "facetFilters": facet_filters if facet_filters else [],
                        "numericFilters": numeric_filters if numeric_filters else [],
                    }]
                }
            )
            
            # Extract first result (we only sent one request)
            result = response.get("results", [{}])[0] if response.get("results") else {}
            
            return {
                "hits": result.get("hits", []),
                "nbHits": result.get("nbHits", 0),
                "page": result.get("page", 0),
                "nbPages": result.get("nbPages", 0),
                "hitsPerPage": result.get("hitsPerPage", limit),
                "processingTimeMS": result.get("processingTimeMS", 0),
                "facets": result.get("facets", {})
            }
        except Exception as e:
            print(f"Algolia search error: {e}")
            return {"hits": [], "nbHits": 0, "error": str(e)}
    
    def search_by_type(
        self,
        component_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search components by type (CPU, GPU, etc.)
        
        Args:
            component_type: Component type to filter by
            filters: Additional filters
            limit: Maximum results
            
        Returns:
            List of matching components
        """
        search_params = {
            "query": "",
            "facetFilters": [f"type:{component_type}"],
            "hitsPerPage": limit,
            "analytics": True,
        }
        
        # Add additional filters
        if filters:
            for key, value in filters.items():
                if key == "socket" and value:
                    search_params["facetFilters"].append(f"socket:{value}")
                elif key == "brand" and value:
                    search_params["facetFilters"].append(f"brand:{value}")
                elif key == "performance_tier" and value:
                    search_params["facetFilters"].append(f"performance_tier:{value}")
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "facetFilters": search_params.get("facetFilters", []),
                        "hitsPerPage": limit,
                        "analytics": True
                    }]
                }
            )
            
            # Extract hits from first result
            results = response.get("results", [{}])[0] if response.get("results") else {}
            return results.get("hits", [])
        except Exception as e:
            print(f"Algolia search by type error: {e}")
            return []
    
    def get_component_by_id(self, component_id: str) -> Optional[Dict]:
        """
        Get a single component by ID
        
        Args:
            component_id: Unique component identifier
            
        Returns:
            Component data or None
        """
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "filters": f"objectID:{component_id}"
                    }]
                }
            )
            results = response.get("results", [{}])[0] if response.get("results") else {}
            hits = results.get("hits", [])
            return hits[0] if hits else None
        except Exception as e:
            print(f"Error fetching component by ID: {e}")
            return None
    
    def get_facets(self, component_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available facet values for filtering
        
        Args:
            component_type: Optional type filter
            
        Returns:
            Dictionary of facet values
        """
        search_params = {
            "query": "",
            "facets": ["brand", "type", "performance_tier", "socket", "memory_type", "form_factor"],
            "hitsPerPage": 0,  # Don't return results, only facets
        }
        
        if component_type:
            search_params["facetFilters"] = [f"type:{component_type}"]
        
        try:
            response = self.search_client.search(
                search_method_params={
                    "requests": [{
                        "indexName": self.index_name,
                        "query": "",
                        "facets": search_params.get("facets", []),
                        "hitsPerPage": 0,
                        "facetFilters": search_params.get("facetFilters", [])
                    }]
                }
            )
            result = response.get("results", [{}])[0] if response.get("results") else {}
            return result.get("facets", {})
        except Exception as e:
            print(f"Error fetching facets: {e}")
            return {}
    
    def index_components(self, components: List[Dict]) -> Dict[str, Any]:
        """
        Index components to Algolia (admin operation)
        
        Args:
            components: List of component dictionaries
            
        Returns:
            Indexing response
        """
        # Ensure each component has objectID
        for component in components:
            if "objectID" not in component:
                component["objectID"] = component.get("id", "")
        
        try:
            response = self.admin_client.save_objects(
                index_name=self.index_name,
                objects=components
            )
            # Handle potential list response (Algolia v4 batching)
            task_ids = []
            object_ids = []
            
            # If response is a list, iterate; if dict, check normally; if object, check attributes
            if isinstance(response, list):
                # Only try to extract info if we really need it, otherwise just success
                return {"success": True, "count": len(components)}
            elif hasattr(response, 'task_id'):
                return {"success": True, "taskID": response.task_id}
            
            # Fallback for dict-like
            return {
                "success": True,
                "taskID": response.get("taskID") if isinstance(response, dict) else None
            }
        except Exception as e:
            print(f"Error indexing components: {e}")
            return {"success": False, "error": str(e)}
    
    def clear_index(self) -> Dict[str, Any]:
        """
        Clear all objects from the index (admin operation)
        
        Returns:
            Clear operation response
        """
        try:
            response = self.admin_client.clear_objects(index_name=self.index_name)
            return {"success": True, "taskID": response.get("taskID")}
        except Exception as e:
            print(f"Error clearing index: {e}")
            return {"success": False, "error": str(e)}
    
    def configure_index_settings(self) -> Dict[str, Any]:
        """
        Configure Algolia index settings for optimal search
        
        Returns:
            Settings update response
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
            return {"success": True, "taskID": response.get("taskID")}
        except Exception as e:
            print(f"Error configuring index settings: {e}")
            return {"success": False, "error": str(e)}

# Create singleton instance
algolia_service = AlgoliaService()
