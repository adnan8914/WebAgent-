# Web Research Agent

A fully functional web research agent that can automatically search the web, find relevant information, extract data from websites, and compile comprehensive research reports based on user queries.

## Features

- **Web Search**: Search the web for information related to user queries
- **Web Scraping**: Extract relevant data from websites
- **Content Analysis**: Analyze and synthesize information from multiple sources
- **News Aggregation**: Find and filter recent news articles on specific topics
- **Report Generation**: Create comprehensive research reports based on gathered information
- **Streamlit Interface**: User-friendly web interface for interacting with the agent

## Architecture

The Web Research Agent is built using the CrewAI framework and consists of the following components:

### Agents

1. **Web Researcher**: Searches the web and extracts information from websites
2. **Content Analyzer**: Analyzes and synthesizes information from multiple sources
3. **Report Writer**: Creates comprehensive research reports based on analyzed information

### Tools

1. **Web Search Tool**: Performs search queries and returns links and snippets
2. **Web Scraper Tool**: Extracts text, structured data, and other relevant information from web pages
3. **Content Analyzer Tool**: Processes and analyzes extracted content for relevance and reliability
4. **News Aggregator Tool**: Finds and filters recent news articles on specific topics

### Tasks

1. **Web Search Task**: Search the web for information related to the user's query
2. **Web Scraping Task**: Extract information from relevant URLs
3. **Content Analysis Task**: Analyze content to extract key information
4. **News Aggregation Task**: Find recent news articles related to the topic
5. **Report Creation Task**: Create a comprehensive research report

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/webagent.git
cd webagent
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the dependencies:
```bash
pip install -e .
```

## Configuration

Before running the agent, you need to set up the required API keys:

1. Create a `.env` file in the root directory of the project:
```bash
touch .env
```

2. Add the following environment variables to the `.env` file:
```
NVIDIA_NIM_API_KEY=your_nvidia_nim_api_key
SERPER_API_KEY=your_serper_api_key
```

3. Replace `your_nvidia_nim_api_key` with your actual NVIDIA NIM API key
4. Replace `your_serper_api_key` with your actual Serper API key

## Usage

### Running the Streamlit App

The easiest way to interact with the Web Research Agent is through the Streamlit interface:

```bash
streamlit run streamlit_app.py
```

This will start a local web server and open the Streamlit interface in your default web browser. You can then enter your research query and the agent will search the web, extract information, and generate a comprehensive report.

### Running the Agent from the Command Line

You can also run the agent directly from the command line:

```bash
python -m webagent.main
```

This will prompt you to enter your research query and will generate a report based on the information found.

## How It Works

1. The user enters a research query through the Streamlit interface
2. The Web Researcher agent searches the web for information related to the query
3. The Web Researcher agent extracts information from relevant websites
4. The Content Analyzer agent analyzes the extracted information
5. The Report Writer agent creates a comprehensive research report
6. The report is displayed in the Streamlit interface and can be downloaded

## Customization

You can customize the agent by modifying the following files:

- `config/agents.yaml`: Define the agents' roles, goals, and backstories
- `config/tasks.yaml`: Define the tasks' descriptions, expected outputs, and assigned agents
- `tools/*.py`: Implement or modify the tools used by the agents

## Troubleshooting

### Common Issues

1. **API Key Not Found**: Make sure you have set the correct API keys in the `.env` file.
2. **Dependencies Installation Failed**: Try installing the dependencies one by one to identify the problematic package.
3. **Streamlit App Not Starting**: Check if the port 8501 is already in use by another application.

### Getting Help

If you encounter any issues not covered in this README, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
