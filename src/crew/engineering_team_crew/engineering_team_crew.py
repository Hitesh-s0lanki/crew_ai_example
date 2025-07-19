from crewai import Agent, Task, Crew
from src.event_listener.custom_event_streamer import CustomStreamEventListener

class EngineeringTeamCrew:
    def __init__(self, openai_llm, gemini_llm):
        # initialize LLM clients
        self.openai_llm = openai_llm
        self.gemini_llm = gemini_llm

        # Define agents
        self._define_agents()
        
        # Define tasks
        self._define_tasks()

    def _define_agents(self):
        self.engineering_lead = Agent(
            llm=self.openai_llm,
            role="Engineering Lead for the engineering team, directing the work of the engineer",
            goal=(
                "Take the high level requirements described here and prepare a detailed design for the backend developer; "
                "everything should be in 1 python module; describe the function and method signatures in the module. "
                "The python module must be completely self-contained, and ready so that it can be tested or have a simple UI built for it. "
                "Here are the requirements: {requirements} "
                "The module should be named {module_name} and the class should be named {class_name}"
            ),
            backstory="You're a seasoned engineering lead with a knack for writing clear and concise designs.",
        )

        self.backend_engineer = Agent(
            llm=self.gemini_llm,
            role="Python Engineer who can write code to achieve the design described by the engineering lead",
            goal=(
                "Write a python module that implements the design described by the engineering lead, in order to achieve the requirements. "
                "The python module must be completely self-contained, and ready so that it can be tested or have a simple UI built for it. "
                "Here are the requirements: {requirements} "
                "The module should be named {module_name} and the class should be named {class_name}"
            ),
            backstory=(
                "You're a seasoned python engineer with a knack for writing clean, efficient code. "
                "You follow the design instructions carefully."
            ),
        )

        self.frontend_engineer = Agent(
            llm=self.gemini_llm,
            role="A Gradio expert to who can write a simple frontend to demonstrate a backend",
            goal=(
                "Write a gradio UI that demonstrates the given backend, all in one file to be in the same directory as the backend module {module_name}. "
                "Here are the requirements: {requirements}"
            ),
            backstory=(
                "You're a seasoned python engineer highly skilled at writing simple Gradio UIs for a backend class. "
                "You produce a simple gradio UI that demonstrates the given backend class; you write the gradio UI in a module app.py that is in the same directory as the backend module {module_name}."
            ),
        )

        self.test_engineer = Agent(
            llm=self.openai_llm,
            role="An engineer with python coding skills who can write unit tests for the given backend module {module_name}",
            goal=(
                "Write unit tests for the given backend module {module_name} and create a test_{module_name} in the same directory as the backend module."
            ),
            backstory="You're a seasoned QA engineer and software developer who writes great unit tests for python code.",
        )

        self.agents = [
            self.engineering_lead,
            self.backend_engineer,
            self.frontend_engineer,
            self.test_engineer,
        ]

    def _define_tasks(self):
        # Design task
        self.design_task = Task(
            description=(
                "Take the high level requirements described here and prepare a detailed design for the engineer; "
                "everything should be in 1 python module, but outline the classes and methods in the module. "
                "Here are the requirements: {requirements} "
                "IMPORTANT: Only output the design in markdown format, laying out in detail the classes and functions in the module, describing the functionality."
            ),
            expected_output="A detailed design for the engineer, identifying the classes and functions in the module.",
            agent=self.engineering_lead,
            markdown=True,
        )

        # Code task
        self.code_task = Task(
            description=(
                "Write a python module that implements the design described by the engineering lead, in order to achieve the requirements. "
                "Here are the requirements: {requirements}"
            ),
            expected_output=(
                "A python module that implements the design and achieves the requirements. "
                "IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks. "
                "The output should be valid Python code that can be directly saved to a file and executed."
            ),
            agent=self.backend_engineer,
            context=[self.design_task],
            markdown=True,
        )

        # Frontend UI task
        self.frontend_task = Task(
            description=(
                "Write a gradio UI in a module app.py that demonstrates the given backend class in {module_name}. "
                "Assume there is only 1 user, and keep the UI very simple indeed - just a prototype or demo. "
                "Here are the requirements: {requirements}"
            ),
            expected_output=(
                "A gradio UI in module app.py that demonstrates the given backend class. "
                "The file should be ready so that it can be run as-is, in the same directory as the backend module, "
                "and it should import the backend class from {module_name}. "
                "IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks. "
                "The output should be valid Python code that can be directly saved to a file and executed."
            ),
            agent=self.frontend_engineer,
            context=[self.code_task],
            markdown=True,
        )

        # Test task
        self.test_task = Task(
            description=(
                "Write unit tests for the given backend module {module_name} and create a test_{module_name} in the same directory as the backend module."
            ),
            expected_output=(
                "A test_{module_name} module that tests the given backend module. "
                "IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, or backticks. "
                "The output should be valid Python code that can be directly saved to a file and executed."
            ),
            agent=self.test_engineer,
            context=[self.code_task],
            markdown=True,
        )

        self.tasks = [
            self.design_task,
            self.code_task,
            self.frontend_task,
            self.test_task,
        ]

    def crew_formation(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            event_listener=CustomStreamEventListener()
        )

    def get_tasks_output(self):
        return {
            "design": self.design_task.output.raw,
            "code": self.code_task.output.raw,
            "frontend": self.frontend_task.output.raw,
            "test": self.test_task.output.raw,
        }
