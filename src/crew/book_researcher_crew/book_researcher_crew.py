import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

from crewai import Agent, Task, Crew
from src.event_listener.custom_event_streamer import CustomStreamEventListener

class BookResearcherCrew:

    def __init__(self, openai_llm, gemini_llm):
        
        load_dotenv()
        os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')
        
        self.agents = []
        self.tasks = [] 
        self.openai_llm = openai_llm
        self.gemini_llm = gemini_llm

    def define_agent(self):
        self.trending_books_agent = Agent(
            llm = self.openai_llm,
            role="""Market Research Agent focused on identifying and analyzing 
            current trending book topics with {genre} genre.""",
            goal="Perform market research to discover the latest trending book topics and high-demand with {genre} genre. Output a Markdown report with key insights, data points, and sources.",
            backstory="""You're a market research specialist with deep knowledge of publishing trends and data analysis.""",
            tools=[SerperDevTool()]
        )

        self.top_novelists_agent= Agent(
            llm = self.openai_llm,
            role="Author Research Agent dedicated to researching top novelists and their upcoming book releases.",
            goal="""Gather information on leading novelists and compile details about their upcoming books, including release dates, descriptions, and patterns. Output a Markdown summary.""",
            backstory="""You're a literary analyst who tracks author careers and publication pipelines.""",
            tools=[SerperDevTool()]
        )
        
        self.genre_research_agent= Agent(
            llm = self.openai_llm,
            role="Genre Deep-Dive Agent specializing in in-depth analysis of a specific book genre.",
            goal="""Conduct a thorough analysis of a {genre} genre, covering market size, audience demographics, key authors, and emerging subgenres. Output findings in Markdown.""",
            backstory="""You're a specialist in genre studies with expertise in market performance and reader behavior.""",
            tools=[SerperDevTool()]
        )

        self.agents.append(self.trending_books_agent)
        self.agents.append(self.top_novelists_agent)
        self.agents.append(self.genre_research_agent)
 
    def define_tasks(self):
        # 1) Trending topics task
        self.trending_topics_task = Task(
            description=(
                "Research and identify the current trending book titles for 2025, "
                "including at least five book names and their publication or anticipated release dates with {genre} genre."
            ),
            expected_output=(
                "A concise Markdown report listing the trending book titles for 2025 with names, dates, "
                "and brief notes, along with genre classification, key insights, data points, and sources."
            ),
            agent=self.trending_books_agent,
            search_query="trending book topics 2025",
            markdown=True,
        )

        # 2) Top novelists task
        self.top_novelists_task = Task(
            description=(
                "Research leading novelists and list their upcoming book releases with {genre} genre, "
                "including release dates and brief descriptions."
            ),
            expected_output="A concise Markdown summary of top novelists and their upcoming books.",
            agent=self.top_novelists_agent,
            markdown=True,
        )

        # 3) Genre research task
        self.genre_research_task = Task(
            description=(
                "For the given genre {genre}, conduct an in-depth market analysis covering "
                "market size, audience demographics, key authors, and emerging subgenres."
            ),
            expected_output="A concise Markdown report detailing genre performance, demographics, authors, and trends.",
            agent=self.genre_research_agent,
            markdown=True,
        )

        # Collect all tasks
        self.tasks.extend([
            self.trending_topics_task,
            self.top_novelists_task,
            self.genre_research_task,
        ])

    def get_tasks_output(self):
        return {
            "trending_topics": self.trending_topics_task.output.raw,
            "top_novelists": self.top_novelists_task.output.raw,
            "genre_research": self.genre_research_task.output.raw,
        }
        
    def crew_formation(self):

        self.define_agent()
        self.define_tasks()

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            event_listener=CustomStreamEventListener()
        )