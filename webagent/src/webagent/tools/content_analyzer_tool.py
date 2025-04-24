from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field
import json
import re


class ContentAnalyzerToolInput(BaseModel):
    """Input schema for ContentAnalyzerTool."""
    content: str = Field(..., description="The content to analyze.")
    analysis_type: str = Field(
        default="summary", 
        description="Type of analysis to perform: 'summary', 'key_points', 'entities', or 'sentiment'."
    )

class ContentAnalyzerTool(BaseTool):
    name: str = "Content Analyzer Tool"
    description: str = (
        "A tool for analyzing content and extracting key information. "
        "It can generate summaries, extract key points, identify entities, or analyze sentiment."
    )
    args_schema: Type[BaseModel] = ContentAnalyzerToolInput

    def _run(self, content: str, analysis_type: str = "summary") -> str:
        """
        Analyze content and extract the requested information.
        
        Args:
            content: The content to analyze
            analysis_type: Type of analysis to perform ('summary', 'key_points', 'entities', or 'sentiment')
            
        Returns:
            A JSON string containing the analysis results
        """
        try:
            result = {}
            
            if analysis_type == "summary":
                result["summary"] = self._generate_summary(content)
            elif analysis_type == "key_points":
                result["key_points"] = self._extract_key_points(content)
            elif analysis_type == "entities":
                result["entities"] = self._identify_entities(content)
            elif analysis_type == "sentiment":
                result["sentiment"] = self._analyze_sentiment(content)
            else:
                # If an unknown analysis type is requested, perform all analyses
                result = {
                    "summary": self._generate_summary(content),
                    "key_points": self._extract_key_points(content),
                    "entities": self._identify_entities(content),
                    "sentiment": self._analyze_sentiment(content)
                }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error analyzing content: {str(e)}"
    
    def _generate_summary(self, content: str) -> str:
        """
        Generate a summary of the content.
        
        Args:
            content: The content to summarize
            
        Returns:
            A summary of the content
        """
        # In a real implementation, this would use NLP techniques or an LLM
        # For this example, we'll create a simple summary
        
        # Split content into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        # If content is too short, return it as is
        if len(sentences) <= 3:
            return content
        
        # Take the first and last sentences, and a middle sentence if available
        summary = sentences[0]
        if len(sentences) > 2:
            summary += " " + sentences[len(sentences) // 2]
        summary += " " + sentences[-1]
        
        return summary
    
    def _extract_key_points(self, content: str) -> List[str]:
        """
        Extract key points from the content.
        
        Args:
            content: The content to analyze
            
        Returns:
            A list of key points
        """
        # In a real implementation, this would use NLP techniques or an LLM
        # For this example, we'll extract sentences that start with key phrases
        
        key_phrases = ["important", "key", "significant", "notable", "critical", "essential"]
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        key_points = []
        for sentence in sentences:
            if any(phrase in sentence.lower() for phrase in key_phrases):
                key_points.append(sentence)
        
        # If no key points were found, take the first few sentences
        if not key_points and sentences:
            key_points = sentences[:min(3, len(sentences))]
        
        return key_points
    
    def _identify_entities(self, content: str) -> Dict[str, List[str]]:
        """
        Identify entities in the content.
        
        Args:
            content: The content to analyze
            
        Returns:
            A dictionary of entity types and their values
        """
        # In a real implementation, this would use NLP techniques or an LLM
        # For this example, we'll use simple regex patterns
        
        entities = {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        }
        
        # Extract people (capitalized words that might be names)
        people_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        entities["people"] = list(set(re.findall(people_pattern, content)))
        
        # Extract organizations (words followed by Inc., Corp., Ltd., etc.)
        org_pattern = r'\b[A-Z][a-zA-Z\s]+(?:Inc\.|Corp\.|Ltd\.|LLC|Company|Association|Organization)\b'
        entities["organizations"] = list(set(re.findall(org_pattern, content)))
        
        # Extract locations (words that might be cities, countries, etc.)
        location_pattern = r'\b[A-Z][a-zA-Z\s]+(?:City|Country|State|Province|Region|Continent)\b'
        entities["locations"] = list(set(re.findall(location_pattern, content)))
        
        # Extract dates (various date formats)
        date_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b'
        entities["dates"] = list(set(re.findall(date_pattern, content)))
        
        return entities
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of the content.
        
        Args:
            content: The content to analyze
            
        Returns:
            A dictionary containing sentiment analysis results
        """
        # In a real implementation, this would use NLP techniques or an LLM
        # For this example, we'll use a simple keyword-based approach
        
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "positive", "beneficial", "advantage", "success", "happy"]
        negative_words = ["bad", "poor", "terrible", "awful", "horrible", "negative", "detrimental", "disadvantage", "failure", "sad"]
        
        positive_count = sum(1 for word in positive_words if word in content.lower())
        negative_count = sum(1 for word in negative_words if word in content.lower())
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = "neutral"
            score = 0.5
        else:
            score = positive_count / total
            if score > 0.6:
                sentiment = "positive"
            elif score < 0.4:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": positive_count,
            "negative_count": negative_count
        } 