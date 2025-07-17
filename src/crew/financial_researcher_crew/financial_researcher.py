import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew

from src.event_listener.custom_event_streamer import CustomStreamEventListener

class FinancialResearcherCrew:

    def __init__(self, openai_llm, gemini_llm):
        load_dotenv()
        os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY')

        self.agents = []
        self.tasks = [] 
        self.openai_llm = openai_llm
        self.gemini_llm = gemini_llm

    def define_agent(self):
        self.research_agent = Agent(
            llm = self.openai_llm,
            role="Senior Financial Researcher for {company}",
            goal="Research the company, news and potential for {company}",
            backstory="""You're a seasoned financial researcher with a talent for finding
            the most relevant information about {company}.
            Known for your ability to find the most relevant
            information and present it in a clear and concise manner.""",
            tools=[SerperDevTool()],
        )

        self.analyst_agent= Agent(
            llm = self.openai_llm,
            role="Market Analyst and Report writer focused on {company}",
            goal=""" Analyze company {company} and create a comprehensive, well-structured report
            that presents insights in a clear and engaging way""",
            backstory=""" You're a meticulous, skilled analyst with a background in financial analysis
            and company research. You have a talent for identifying patterns and extracting
            meaningful insights from research data, then communicating
            those insights through well crafted reports""",
            tools=[SerperDevTool()],
        )

        self.agents.append(self.research_agent)
        self.agents.append(self.analyst_agent)
 
    def define_task(self):
        self.research_task = Task(
            description="""Conduct thorough research on company {company}. Focus on:
            1. Current company status and health
            2. Historical company performance
            3. Major challenges and opportunities
            4. Recent news and events
            5. Future outlook and potential developments

            Make sure to organize your findings in a structured format with clear sections.""",
            expected_output=""" A comprehensive research document with well-organized sections covering
            all the requested aspects of {company}. Include specific facts, figures,
            and examples where relevant.""",
            agent=self.research_agent
        )

        self.analysis_task = Task(
            description="""Analyze the research findings and create a comprehensive report on {company}.
            Your report should:
            1. Begin with an executive summary
            2. Include all key information from the research
            3. Provide insightful analysis of trends and patterns
            4. Offer a market outlook for company, noting that this should not be used for trading decisions
            5. Be formatted in a professional, easy-to-read style with clear headings""",
            expected_output="""  A polished, professional report on {company} that presents the research
            findings with added analysis and insights. The report should be well-structured
            with an executive summary, main sections, and conclusion.""",
            agent=self.analyst_agent
        )

        self.tasks.append(self.research_task)
        self.tasks.append(self.analysis_task)

    
    def crew_formation(self):

        self.define_agent()
        self.define_task()

        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            event_listener=CustomStreamEventListener()
        )

        return crew
    
        