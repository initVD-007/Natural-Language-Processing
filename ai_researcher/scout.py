import requests
import json
import asyncio
import aiohttp
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

class AgentB_Scout:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Serper API Key is required.")
        self.api_key = api_key

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(aiohttp.ClientError))
    async def fetch_serper_async(self, session, query):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        async with session.post(url, headers=headers, data=payload, timeout=10) as response:
            response.raise_for_status()
            return await response.json()

    async def search_2026_async(self, queries):
        """Goes to the web and returns real-time data for each query asynchronously."""
        all_results = []
        
        async def process_query(session, q):
            try:
                data = await self.fetch_serper_async(session, q)
                organic_results = data.get('organic', [])
                if not organic_results:
                    snippets = ["No specific results found for this query."]
                else:
                    snippets = [item.get('snippet', '') for item in organic_results]
                
                return {"query": q, "findings": snippets[:3]}
            except Exception as e:
                return {"query": q, "findings": [f"Search request failed after retries: {str(e)}"]}

        async with aiohttp.ClientSession() as session:
            tasks = [process_query(session, q) for q in queries]
            all_results = await asyncio.gather(*tasks)
            
        return all_results

    def search_2026(self, queries):
        """Wrapper method for backward compatibility."""
        return asyncio.run(self.search_2026_async(queries))