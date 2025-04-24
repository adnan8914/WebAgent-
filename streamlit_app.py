
import sys
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# ✅ Then continue with other imports
from run_app import main
#!/usr/bin/env python
import streamlit as st
import os
import time
from datetime import datetime
import json
from dotenv import load_dotenv
from run_app import main


# Load environment variables from .env file
load_dotenv()

# Import CrewAI components
from crewai import Agent, Task, Crew, Process
from webagent.tools import WebSearchTool, WebScraperTool, ContentAnalyzerTool, NewsAggregatorTool

def create_web_research_crew(query, days=7):
    """
    Create a web research crew with the necessary agents and tasks.
    
    Args:
        query: The user's research query
        days: Number of days to look back for news articles
        
    Returns:
        A configured Crew object
    """
    # Extract topic from query for better organization
    topic = " ".join(query.split()[0:3])  # Use first few words as topic
    
    # Create agents
    web_researcher = Agent(
        role="Web Researcher",
        goal="Search the web for relevant information about the given topic",
        backstory="You are an expert web researcher with years of experience in finding accurate and relevant information online.",
        tools=[WebSearchTool(), WebScraperTool(), NewsAggregatorTool()],
        verbose=True
    )
    
    content_analyzer = Agent(
        role="Content Analyzer",
        goal="Analyze and extract key information from web content",
        backstory="You are a skilled content analyst who can identify the most important information from various sources.",
        tools=[ContentAnalyzerTool()],
        verbose=True
    )
    
    report_writer = Agent(
        role="Report Writer",
        goal="Compile research findings into a comprehensive report",
        backstory="You are a professional report writer who can synthesize information from multiple sources into a clear, well-structured report.",
        verbose=True
    )
    
    # Create tasks
    web_search_task = Task(
        description=f"Search the web for information about: {query}",
        agent=web_researcher,
        expected_output="A list of relevant web pages and their content related to the query."
    )
    
    web_scraping_task = Task(
        description=f"Extract detailed information from the web pages found about: {query}",
        agent=web_researcher,
        expected_output="Detailed information extracted from the web pages.",
        context=[web_search_task]
    )
    
    news_aggregation_task = Task(
        description=f"Find recent news articles (within the last {days} days) about: {query}",
        agent=web_researcher,
        expected_output="A summary of recent news articles related to the query."
    )
    
    content_analysis_task = Task(
        description=f"Analyze the content gathered about: {query}",
        agent=content_analyzer,
        expected_output="Key insights and information extracted from the content.",
        context=[web_scraping_task, news_aggregation_task]
    )
    
    report_creation_task = Task(
        description=f"Create a comprehensive research report about: {query}",
        agent=report_writer,
        expected_output="A well-structured research report that answers the query.",
        context=[content_analysis_task]
    )
    
    # Create crew
    crew = Crew(
        agents=[web_researcher, content_analyzer, report_writer],
        tasks=[web_search_task, web_scraping_task, news_aggregation_task, content_analysis_task, report_creation_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

def run_web_research(query, days=7, show_intermediate=False):
    """
    Run the web research crew with a user query.
    
    Args:
        query: The user's research query
        days: Number of days to look back for news articles
        show_intermediate: Whether to show intermediate results
        
    Returns:
        The path to the generated report and intermediate results if requested
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if NVIDIA NIM API key is set
    if not os.environ.get("NVIDIA_NIM_API_KEY"):
        raise Exception("NVIDIA NIM API key not found. Please set the NVIDIA_NIM_API_KEY environment variable.")
    
    # Set the model provider to NVIDIA
    os.environ["MODEL_PROVIDER"] = "nvidia"
    
    # Create a directory for intermediate results if needed
    intermediate_results = {}
    if show_intermediate:
        os.makedirs("intermediate_results", exist_ok=True)
    
    try:
        # Create the crew
        crew = create_web_research_crew(query, days)
        
        # Run the crew with task callbacks if intermediate results are requested
        if show_intermediate:
            def task_callback(task_output, task):
                task_name = task.name
                # Convert task_output to string if it's not already
                if not isinstance(task_output, str):
                    task_output = str(task_output)
                intermediate_results[task_name] = task_output
                
                # Save the intermediate result to a file
                with open(f"intermediate_results/{task_name}.json", "w") as f:
                    json.dump({"task": task_name, "output": task_output}, f, indent=2)
                
                return task_output
            
            result = crew.kickoff(task_callbacks=[task_callback])
        else:
            result = crew.kickoff()
        
        # Convert result to string if it's not already
        if not isinstance(result, str):
            result = str(result)
        
        # Save the result to a file
        report_path = "research_report.md"
        with open(report_path, "w") as f:
            f.write(result)
        
        if show_intermediate:
            return report_path, intermediate_results
        else:
            return report_path
    except Exception as e:
        # Handle the specific error we're seeing
        if "cannot schedule new futures after shutdown" in str(e):
            # Create a simple report with the error message
            report_path = "research_report.md"
            with open(report_path, "w") as f:
                f.write(f"# Research Report\n\n")
                f.write(f"## Error\n\n")
                f.write(f"An error occurred while running the web research: {str(e)}\n\n")
                f.write(f"## Possible Solutions\n\n")
                f.write(f"1. Restart the Streamlit app\n")
                f.write(f"2. Try a simpler query\n")
                f.write(f"3. Check your NVIDIA NIM API key\n")
            
            if show_intermediate:
                return report_path, {"error": str(e)}
            else:
                return report_path
        else:
            raise Exception(f"An error occurred while running the web research: {e}")

def main():
    """
    Run the Streamlit app for the web research agent.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    st.set_page_config(
        page_title="Web Research Agent",
        page_icon="🔍",
        layout="wide"
    )
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for settings
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Check if NVIDIA NIM API key is set
        api_key = os.environ.get("NVIDIA_NIM_API_KEY", "")
        if not api_key:
            st.error("NVIDIA NIM API key not found. Please set the NVIDIA_NIM_API_KEY environment variable.")
            st.stop()
        
        # Advanced options
        days = st.slider("Look back period for news (days):", min_value=1, max_value=30, value=7)
        show_intermediate = st.checkbox("Show intermediate results", value=False)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This agent can automatically search the web, find relevant information, extract data from websites, 
        and compile comprehensive research reports based on your questions.
        
        The agent uses NVIDIA NIM models for processing and generating content.
        """)
    
    # Main chat interface
    st.title("🔍 Web Research Agent")
    st.markdown("Ask any question, and I'll search the web to find the answer for you.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching the web... This may take a few minutes."):
                try:
                    # Run the web research
                    if show_intermediate:
                        report_path, intermediate_results = run_web_research(prompt, days, show_intermediate=True)
                    else:
                        report_path = run_web_research(prompt, days)
                    
                    # Read the report
                    with open(report_path, "r") as f:
                        report_content = f.read()
                    
                    # Display the report
                    st.markdown(report_content)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": report_content})
                    
                    # Download button for the report
                    st.download_button(
                        label="Download Report",
                        data=report_content,
                        file_name="research_report.md",
                        mime="text/markdown"
                    )
                    
                    # Display intermediate results if requested
                    if show_intermediate:
                        with st.expander("View Research Process"):
                            # Create tabs for each intermediate result
                            tabs = st.tabs([f"Step {i+1}: {task_name}" for i, task_name in enumerate(intermediate_results.keys())])
                            
                            for i, (task_name, result) in enumerate(intermediate_results.items()):
                                with tabs[i]:
                                    st.markdown(f"### {task_name}")
                                    st.text(result)
                                    
                                    # Download button for the intermediate result
                                    st.download_button(
                                        label=f"Download {task_name} Result",
                                        data=result,
                                        file_name=f"{task_name}.txt",
                                        mime="text/plain",
                                        key=f"download_{i}"
                                    )
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main() 
