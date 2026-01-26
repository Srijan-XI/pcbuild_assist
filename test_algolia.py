import sys
sys.path.append('P:/DEV-CHALLENGE/CFNC/backend')

from app.services.algolia_service import algolia_service

try:
    # Test basic search
    response = algolia_service.search_client.search(
        search_method_params={
            "requests": [{
                "indexName": "pc_components",
                "query": "",
                "hitsPerPage": 1
            }]
        }
    )
    
    print("Response type:", type(response))
    print("Has results attr:", hasattr(response, 'results'))
    
    if hasattr(response, 'results'):
        print("Results type:", type(response.results))
        print("Results length:", len(response.results))
        if response.results:
            r = response.results[0]
            print("First result type:", type(r))
            
            # Try actual_instance
            if hasattr(r, 'actual_instance'):
                actual = r.actual_instance
                print("Actual instance type:", type(actual))
                print("Actual instance attrs:", [a for a in dir(actual) if not a.startswith('_')])
                if hasattr(actual, 'nb_hits'):
                    print("Total hits:", actual.nb_hits)
                if hasattr(actual, 'hits'):
                    print("Hits count:", len(actual.hits))
                    if actual.hits:
                        print("First hit keys:", list(actual.hits[0].keys()) if isinstance(actual.hits[0], dict) else 'not a dict')

    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
