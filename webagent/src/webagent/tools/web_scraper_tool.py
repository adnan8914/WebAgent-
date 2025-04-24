from crewai.tools import BaseTool
from typing import Type, Dict, Any, Optional, List
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse


class WebScraperToolInput(BaseModel):
    """Input schema for WebScraperTool."""
    url: str = Field(..., description="The URL of the webpage to scrape.")
    extract_type: str = Field(
        default="text", 
        description="Type of content to extract: 'text', 'links', 'tables', or 'all'."
    )

class WebScraperTool(BaseTool):
    name: str = "Web Scraper Tool"
    description: str = (
        "A tool for extracting information from web pages. "
        "It can extract text content, links, tables, or all of the above from a given URL."
    )
    args_schema: Type[BaseModel] = WebScraperToolInput

    def _run(self, url: str, extract_type: str = "text") -> str:
        """
        Scrape a webpage and extract the requested information.
        
        Args:
            url: The URL of the webpage to scrape
            extract_type: Type of content to extract ('text', 'links', 'tables', or 'all')
            
        Returns:
            A JSON string containing the extracted information
        """
        try:
            # Validate URL
            if not self._is_valid_url(url):
                return json.dumps({"error": f"Invalid URL: {url}"}, indent=2)
            
            # Add a small delay to be respectful to websites
            time.sleep(1)
            
            # Fetch the webpage
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                return json.dumps({"error": f"Failed to fetch URL: {str(e)}"}, indent=2)
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the requested information
            result = {}
            
            if extract_type in ["text", "all"]:
                # Extract main text content
                result["text"] = self._extract_text(soup)
            
            if extract_type in ["links", "all"]:
                # Extract links
                result["links"] = self._extract_links(soup, url)
            
            if extract_type in ["tables", "all"]:
                # Extract tables
                result["tables"] = self._extract_tables(soup)
            
            # Extract metadata
            result["metadata"] = self._extract_metadata(soup)
            
            # If no specific type was requested or found, return a basic summary
            if not result:
                result["summary"] = f"Could not extract {extract_type} from {url}. The page title is: {soup.title.string if soup.title else 'No title found'}"
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error scraping webpage: {str(e)}"}, indent=2)
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if the URL is valid.
        
        Args:
            url: The URL to check
            
        Returns:
            True if the URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extract the main text content from the HTML.
        
        Args:
            soup: The BeautifulSoup object
            
        Returns:
            The extracted text
        """
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit text length
        if len(text) > 10000:
            text = text[:10000] + "..."
        
        return text
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """
        Extract links from the HTML.
        
        Args:
            soup: The BeautifulSoup object
            base_url: The base URL for resolving relative links
            
        Returns:
            A list of links with text and URL
        """
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Resolve relative URLs
            if not href.startswith(('http://', 'https://')):
                href = urljoin(base_url, href)
            
            # Skip anchor links
            if href.startswith('#'):
                continue
                
            # Skip javascript links
            if href.startswith('javascript:'):
                continue
                
            links.append({
                "text": a.text.strip() or href,
                "url": href
            })
        
        # Limit to 20 links
        return links[:20]
    
    def _extract_tables(self, soup: BeautifulSoup) -> List[List[List[str]]]:
        """
        Extract tables from the HTML.
        
        Args:
            soup: The BeautifulSoup object
            
        Returns:
            A list of tables, each table is a list of rows, each row is a list of cells
        """
        tables = []
        for table in soup.find_all('table'):
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if cols:
                    table_data.append([col.text.strip() for col in cols])
            if table_data:
                tables.append(table_data)
        
        # Limit to 5 tables
        return tables[:5]
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract metadata from the HTML.
        
        Args:
            soup: The BeautifulSoup object
            
        Returns:
            A dictionary of metadata
        """
        metadata = {}
        
        # Extract title
        if soup.title:
            metadata["title"] = soup.title.string
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and 'content' in meta_desc.attrs:
            metadata["description"] = meta_desc['content']
        
        # Extract meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and 'content' in meta_keywords.attrs:
            metadata["keywords"] = meta_keywords['content']
        
        # Extract Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        for tag in og_tags:
            if 'property' in tag.attrs and 'content' in tag.attrs:
                property_name = tag['property'].replace('og:', '')
                metadata[f"og_{property_name}"] = tag['content']
        
        return metadata 