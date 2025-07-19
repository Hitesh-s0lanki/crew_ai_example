## Stream Response through fastapi 
import asyncio

from crewai.utilities.events.base_event_listener import BaseEventListener

# Import only the events you care about
from crewai.utilities.events.agent_events import AgentExecutionStartedEvent
from crewai.utilities.events.llm_events import (
    LLMCallStartedEvent,
    LLMCallCompletedEvent,
)
from crewai.utilities.events.tool_usage_events import (
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent,
)
from crewai.utilities.events.crew_events import CrewKickoffStartedEvent, CrewKickoffCompletedEvent

# shared queue for all events
event_queue: asyncio.Queue[dict] = asyncio.Queue()

class CustomStreamEventListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):

        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_kickoff_started(source, event: CrewKickoffStartedEvent):
            payload = {
                "title": "Crew Kickoff",
                "type": "crew",
                "response": f"User: {event.inputs}"
            }
            event_queue.put_nowait(payload)

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_kickoff_completed(source, event: CrewKickoffCompletedEvent):
            print("Crew Work Completed Successfully")
            payload = {
                "title": "Crew Completed",
                "type": "agent",
                "response": f"{event.output}"
            }
            event_queue.put_nowait(payload)

        # Agent execution
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def _on_agent_execution_started(source, event: AgentExecutionStartedEvent):
            print(f"[AgentExecutionStartedEvent] Agent {event.agent.role} started task.")
            print(f"prompt for the agent : {event.task_prompt}")
            payload = {
                "title": "Agent Execution",
                "type": "agent",
                "response": f"{event.agent.role} started with prompt: {event.task_prompt}"
            }
            event_queue.put_nowait(payload)

        # LLM calls and streaming
        @crewai_event_bus.on(LLMCallStartedEvent)
        def _on_llm_call_started(source, event: LLMCallStartedEvent):
            print(f"[LLMCallStartedEvent] Prompt sent to LLM.")
            payload = {
                "title": "LLM Call",
                "type": "llm",
                "response": f"{event.messages[-1].content}"
            }
            event_queue.put_nowait(payload)

        # @crewai_event_bus.on(LLMCallCompletedEvent)
        def _on_llm_call_completed(source, event: LLMCallCompletedEvent):
            print(f"[LLMCallCompletedEvent] Full response received. {event.response}")
            payload = {
                "title": "LLM Response",
                "type": "llm",
                "response": event.response
            }
            event_queue.put_nowait(payload)

        # Tool usage
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def _on_tool_usage_started(source, event: ToolUsageStartedEvent):
            print(f"[ToolUsageStartedEvent] Calling tool: {event.tool_name}")
            payload = {
                "title": "Tool Started",
                "type": "tool",
                "response": f"Calling {event.tool_name}"
            }
            event_queue.put_nowait(payload)

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def _on_tool_usage_finished(source, event: ToolUsageFinishedEvent):
            print(f"[ToolUsageFinishedEvent] Tool {event.output} finished.")
            payload = {
                "title": "Tool Finished",
                "type": "tool",
                "response": f"{event.tool_name} output → {event.output}"
            }
            event_queue.put_nowait(payload)