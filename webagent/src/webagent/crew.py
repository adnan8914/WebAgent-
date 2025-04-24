from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from webagent.tools import WebSearchTool, WebScraperTool, ContentAnalyzerTool, NewsAggregatorTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Webagent():
    """Webagent crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )
    
    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_researcher'],
            tools=[WebSearchTool(), WebScraperTool(), NewsAggregatorTool()],
            verbose=True
        )
    
    @agent
    def content_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_analyzer'],
            tools=[ContentAnalyzerTool()],
            verbose=True
        )
    
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )
    
    @task
    def web_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_search_task'],
        )
    
    @task
    def web_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scraping_task'],
        )
    
    @task
    def content_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_analysis_task'],
        )
    
    @task
    def news_aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_aggregation_task'],
        )
    
    @task
    def report_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_creation_task'],
            output_file='research_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Webagent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
