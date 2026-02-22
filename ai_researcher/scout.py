import requests
import json

class AgentB_Scout:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Serper API Key is required.")
        self.api_key = api_key

    def search_2026(self, queries):
        """Goes to the web and returns real-time data for each query."""
        all_results = []
        
        for q in queries:
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": q})
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Extract just the snippets (the useful text)
                organic_results = data.get('organic', [])
                if not organic_results:
                    snippets = ["No specific results found for this query."]
                else:
                    snippets = [item.get('snippet', '') for item in organic_results]
                
                all_results.append({"query": q, "findings": snippets[:3]}) # Top 3 per query
            except requests.exceptions.RequestException as e:
                all_results.append({"query": q, "findings": [f"Search request failed: {str(e)}"]})
            
        return all_results