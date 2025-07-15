from typing import Optional
from crewai.utilities.events.base_event_listener import BaseEventListener

# Import only the events you care about
from crewai.utilities.events.agent_events import AgentExecutionStartedEvent
from crewai.utilities.events.task_events import (
    TaskStartedEvent,
    TaskCompletedEvent,
    TaskEvaluationEvent,
)
from crewai.utilities.events.llm_events import (
    LLMCallStartedEvent,
    LLMStreamChunkEvent,
    LLMCallCompletedEvent,
)
from crewai.utilities.events.tool_usage_events import (
    ToolUsageStartedEvent,
    ToolUsageFinishedEvent,
)
from crewai.utilities.events.knowledge_events import KnowledgeRetrievalStartedEvent
from crewai.utilities.events.crew_events import CrewKickoffStartedEvent, CrewKickoffCompletedEvent

try:
    import agentops
    AGENTOPS_INSTALLED = True
except ImportError:
    AGENTOPS_INSTALLED = False


class PrintAllEventsListener(BaseEventListener):

    tool_event: Optional["agentops.ToolEvent"] = None
    session: Optional["agentops.Session"] = None

    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        if not AGENTOPS_INSTALLED:
            return

        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_kickoff_started(source, event: CrewKickoffStartedEvent):
            self.session = agentops.init()
            for agent in source.agents:
                if self.session:
                    self.session.create_agent(
                        name=agent.role,
                        agent_id=str(agent.id),
                    )

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_kickoff_completed(source, event: CrewKickoffCompletedEvent):
            if self.session:
                self.session.end_session(
                    end_state="Success",
                    end_state_reason="Finished Execution",
                )

        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_usage_started(source, event: ToolUsageStartedEvent):
            self.tool_event = agentops.ToolEvent(name=event.tool_name)
            if self.session:
                self.session.record(self.tool_event)

        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def _on_kickoff_started(source, event: CrewKickoffStartedEvent):
            print(f"[CrewKickoffStartedEvent] Starting crew…")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def _on_kickoff_completed(source, event: CrewKickoffCompletedEvent):
            print(f"[CrewKickoffCompletedEvent] Crew finished successfully.")

        # Agent execution
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def _on_agent_execution_started(source, event: AgentExecutionStartedEvent):
            print(f"[AgentExecutionStartedEvent] Agent {event.agent_id} started task.")

        # Task lifecycle
        @crewai_event_bus.on(TaskStartedEvent)
        def _on_task_started(source, event: TaskStartedEvent):
            print(f"[TaskStartedEvent] Task {event.task} started.")

        @crewai_event_bus.on(TaskCompletedEvent)
        def _on_task_completed(source, event: TaskCompletedEvent):
            print(f"[TaskCompletedEvent] Task {event.task} completed.")

        @crewai_event_bus.on(TaskEvaluationEvent)
        def _on_task_evaluation(source, event: TaskEvaluationEvent):
            print(f"[TaskEvaluationEvent] Task {event.task} evaluated.")

        # LLM calls and streaming
        @crewai_event_bus.on(LLMCallStartedEvent)
        def _on_llm_call_started(source, event: LLMCallStartedEvent):
            print(f"[LLMCallStartedEvent] Prompt sent to LLM.")

        @crewai_event_bus.on(LLMStreamChunkEvent)
        def _on_llm_stream_chunk(source, event: LLMStreamChunkEvent):
            print(f"[LLMStreamChunkEvent] Received chunk: {event.token!r}")

        @crewai_event_bus.on(LLMCallCompletedEvent)
        def _on_llm_call_completed(source, event: LLMCallCompletedEvent):
            print(f"[LLMCallCompletedEvent] Full response received.")

        # Tool usage
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def _on_tool_usage_started(source, event: ToolUsageStartedEvent):
            print(f"[ToolUsageStartedEvent] Calling tool: {event.tool_name}")

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def _on_tool_usage_finished(source, event: ToolUsageFinishedEvent):
            print(f"[ToolUsageFinishedEvent] Tool {event.tool_name} finished.")

        # Knowledge retrieval
        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def _on_knowledge_retrieval_started(source, event: KnowledgeRetrievalStartedEvent):
            print(f"[KnowledgeRetrievalStartedEvent] Retrieving from knowledge base…")
