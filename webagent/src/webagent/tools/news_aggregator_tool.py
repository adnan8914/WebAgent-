from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field
import json
import datetime


class NewsAggregatorToolInput(BaseModel):
    """Input schema for NewsAggregatorTool."""
    topic: str = Field(..., description="The topic to search for news articles.")
    days: int = Field(default=7, description="Number of days to look back for news articles.")
    max_results: int = Field(default=5, description="Maximum number of news articles to return.")

class NewsAggregatorTool(BaseTool):
    name: str = "News Aggregator Tool"
    description: str = (
        "A tool for finding and filtering recent news articles on specific topics. "
        "It returns a list of news articles with titles, summaries, sources, and publication dates."
    )
    args_schema: Type[BaseModel] = NewsAggregatorToolInput

    def _run(self, topic: str, days: int = 7, max_results: int = 5) -> str:
        """
        Find recent news articles on a specific topic.
        
        Args:
            topic: The topic to search for news articles
            days: Number of days to look back for news articles
            max_results: Maximum number of news articles to return
            
        Returns:
            A JSON string containing news articles
        """
        try:
            # In a real implementation, this would use a news API
            # For this example, we'll simulate news articles
            articles = self._simulate_news_articles(topic, days, max_results)
            return json.dumps(articles, indent=2)
        except Exception as e:
            return f"Error finding news articles: {str(e)}"
    
    def _simulate_news_articles(self, topic: str, days: int, max_results: int) -> List[Dict[str, Any]]:
        """
        Simulate news articles for demonstration purposes.
        In a real implementation, this would be replaced with an actual API call.
        
        Args:
            topic: The topic to search for news articles
            days: Number of days to look back for news articles
            max_results: Maximum number of news articles to return
            
        Returns:
            A list of news articles
        """
        # Generate random dates within the specified range
        today = datetime.datetime.now()
        dates = [
            today - datetime.timedelta(days=i)
            for i in range(days)
        ]
        
        # Generate random news articles
        articles = []
        for i in range(min(max_results, len(dates))):
            date = dates[i]
            formatted_date = date.strftime("%B %d, %Y")
            
            # Generate different types of news articles based on the topic
            if "technology" in topic.lower():
                title = f"New {topic} Innovation Announced"
                summary = f"A groundbreaking development in {topic} has been announced. Experts say this could revolutionize the industry."
                source = "Tech News Daily"
            elif "science" in topic.lower():
                title = f"Scientists Make Breakthrough in {topic} Research"
                summary = f"Researchers have made a significant discovery in the field of {topic}. The findings were published in a leading scientific journal."
                source = "Science Today"
            elif "business" in topic.lower():
                title = f"Market Analysis: {topic} Industry Trends"
                summary = f"Recent market data shows significant growth in the {topic} sector. Analysts predict continued expansion in the coming years."
                source = "Business Insider"
            elif "health" in topic.lower():
                title = f"New Study Reveals Health Benefits of {topic}"
                summary = f"A comprehensive study has found that {topic} may have unexpected health benefits. Medical experts are reviewing the findings."
                source = "Health News"
            else:
                title = f"Latest Developments in {topic}"
                summary = f"Recent developments in {topic} have captured the attention of experts and the public alike. Here's what you need to know."
                source = "General News"
            
            articles.append({
                "title": title,
                "summary": summary,
                "source": source,
                "date": formatted_date,
                "url": f"https://example.com/news/{i+1}"
            })
        
        return articles 