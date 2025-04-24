from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import json


class WebSearchToolInput(BaseModel):
    """Input schema for WebSearchTool."""
    query: str = Field(..., description="The search query to look up on the web.")
    num_results: int = Field(default=5, description="Number of search results to return.")

class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "A tool for searching the web for information related to a query. "
        "It returns a list of search results with titles, snippets, and URLs."
    )
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str, num_results: int = 5) -> str:
        """
        Perform a web search and return the results.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            A JSON string containing search results
        """
        try:
            # Use the Serper API to perform a real web search
            results = self._search_with_serper(query, num_results)
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def _search_with_serper(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Perform a web search using the Serper API.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            A list of search results
        """
        # Serper API endpoint
        url = "https://google.serper.dev/search"
        
        # API key
        api_key = "cbc147345d839e169a160ae417b9929650634598"
        
        # Headers
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        # Payload
        payload = {
            "q": query,
            "num": num_results
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        # Extract the organic search results
        if "organic" in data:
            results = []
            for item in data["organic"][:num_results]:
                result = {
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", "")
                }
                results.append(result)
            return results
        else:
            # If no organic results, return an empty list
            return []
    
    def _simulate_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Simulate search results for demonstration purposes.
        This is kept as a fallback in case the API call fails.
        """
        # This is a placeholder implementation
        # In a real application, you would use a search API like Google Custom Search
        results = []
        
        # Simulate different types of queries
        if "news" in query.lower():
            results = [
                {
                    "title": f"Latest News on {query} - {i+1}",
                    "snippet": f"This is a simulated news article about {query}. It contains relevant information that would be useful for research.",
                    "url": f"https://example.com/news/{i+1}"
                } for i in range(num_results)
            ]
        elif "research" in query.lower():
            results = [
                {
                    "title": f"Research Paper on {query} - {i+1}",
                    "snippet": f"This is a simulated research paper about {query}. It contains detailed analysis and findings.",
                    "url": f"https://example.com/research/{i+1}"
                } for i in range(num_results)
            ]
        else:
            results = [
                {
                    "title": f"Information about {query} - {i+1}",
                    "snippet": f"This is a simulated webpage about {query}. It contains general information that would be useful for research.",
                    "url": f"https://example.com/info/{i+1}"
                } for i in range(num_results)
            ]
        
        return results 