import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class AgentB_Scout:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")

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
            
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            
            # Extract just the snippets (the useful text)
            snippets = [item.get('snippet', '') for item in data.get('organic', [])]
            all_results.append({"query": q, "findings": snippets[:3]}) # Top 3 per query
            
        return all_results