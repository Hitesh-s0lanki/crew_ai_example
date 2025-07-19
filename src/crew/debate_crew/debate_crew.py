from crewai import Agent, Task, Crew
from src.event_listener.custom_event_streamer import CustomStreamEventListener

class DebaterCrew:

    def __init__(self, openai_llm, gemini_llm):
        self.agents = []
        self.tasks = [] 
        self.openai_llm = openai_llm
        self.gemini_llm = gemini_llm

    def define_agent(self):
        self.debater = Agent(
            llm = self.openai_llm,
            role="A compelling debater",
            goal="Present a clear argument either in favor of or against the motion. The motion is: {motion}",
            backstory="""You're an experienced debator with a knack for giving concise but convincing arguments.
            The motion is: {motion}"""
        )

        self.judge= Agent(
            llm = self.openai_llm,
            role="Decide the winner of the debate based on the arguments presented",
            goal="""Given arguments for and against this motion: {motion}, decide which side is more convincing,
                    based purely on the arguments presented.""",
            backstory="""You are a fair judge with a reputation for weighing up arguments without factoring in
            your own views, and making a decision based purely on the merits of the argument.
            The motion is: {motion}""",
        )

        self.agents.append(self.debater)
        self.agents.append(self.judge)
 
    def define_task(self):
        self.propose = Task(
            description="""You are proposing the motion: {motion}.
            Come up with a clear argument in favor of the motion.
            Be very convincing.""",
            expected_output="""Your clear argument in favor of the motion, in a concise manner.""",
            agent=self.debater
        )
        
        self.oppose = Task(
            description="""You are in opposition to the motion: {motion}.
            Come up with a clear argument against the motion.
            Be very convincing.""",
            expected_output="""Your clear argument against the motion, in a concise manner.""",
            agent=self.debater,
            markdown=True # Output formatted as markdown for clarity
        )

        self.decide = Task(
            description="""Review the arguments presented by the debaters and decide 
            which side is more convincing.""",
            expected_output="""Your decision on which side is more convincing, and why.""",
            agent=self.judge,
            markdown=True # Output formatted as markdown for clarity
        )

        self.tasks.append(self.propose)
        self.tasks.append(self.oppose)
        self.tasks.append(self.decide)

    def get_tasks_output(self):
        return {
            "propose": self.propose.output.raw,
            "oppose": self.oppose.output.raw,
            "decide": self.decide.output.raw
        }
    
    def crew_formation(self):

        self.define_agent()
        self.define_task()

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            event_listener=CustomStreamEventListener()
        )