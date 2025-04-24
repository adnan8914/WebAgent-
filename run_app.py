#!/usr/bin/env python
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function for the Streamlit app."""
    st.set_page_config(
        page_title="Web Research Agent",
        page_icon="🔍",
        layout="wide"
    )
    
    # Header
    st.title("🔍 Web Research Agent")
    st.markdown("A powerful web research tool that can search the web, analyze content, and create comprehensive reports.")
    
    # Check if API keys are available
    serper_key = os.environ.get("SERPER_API_KEY")
    nvidia_key = os.environ.get("NVIDIA_NIM_API_KEY")
    
    if not serper_key or not nvidia_key:
        st.warning("⚠️ API keys missing. Please configure them in Streamlit secrets.")
        st.info("The application needs SERPER_API_KEY and NVIDIA_NIM_API_KEY to function.")
        return
    
    # Main input area
    query = st.text_input("What would you like to research?", placeholder="Enter a research topic...")
    search_button = st.button("Start Research", type="primary")
    
    if search_button and query:
        st.info("This is a placeholder. The actual implementation would use CrewAI to perform web research.")
        st.code(f"Query: {query}\nSerper Key available: {bool(serper_key)}\nNVIDIA Key available: {bool(nvidia_key)}")

if __name__ == "__main__":
    main() 