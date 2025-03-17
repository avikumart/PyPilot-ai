from contextlib import ExitStack
from functools import partial, wraps
from typing import Any, Callable, Optional

from pydantic import Field, field_validator

from controlflow.agents.agent import Agent, BaseAgent
from controlflow.events.base import Event
from controlflow.events.message_compiler import MessageCompiler
from controlflow.flows import Flow
from controlflow.llm.messages import BaseMessage
from controlflow.orchestration.handler import Handler
from controlflow.tasks.task import Task
from controlflow.tools.tools import Tool, as_tools
from controlflow.utilities.context import ctx
from controlflow.utilities.general import ControlFlowModel

__all__ = [
    "AgentContext",
    "get_context",
    "provide_agent_context",
]


class AgentContext(ControlFlowModel):
    """
    The full context for an invocation of a BaseAgent
    """

    model_config = dict(arbitrary_types_allowed=True)
    flow: Flow
    tasks: list[Task]
    tools: list[Any] = []
    agents: list[BaseAgent] = Field(
        default_factory=list,
        description="Any other agents that are relevant to this operation, in order to properly load events",
    )
    handlers: list[Handler] = []
    instructions: list[str] = []
    _context: Optional[ExitStack] = None

    @field_validator("tools", mode="before")
    def _validate_tools(cls, v):
        if v:
            v = as_tools(v)
        return v

    def add_agent(self, agent: BaseAgent):
        if agent not in self.agents:
            self.agents = self.agents + [agent]

    def handle_event(self, event: Event, persist: bool = None):
        if persist is None:
            persist = event.persist

        event.thread_id = self.flow.thread_id
        event.add_tasks(self.tasks)
        event.add_agents(self.agents)

        for handler in self.handlers:
            handler.handle(event)
        if persist:
            self.flow.add_events([event])

    def add_handlers(self, handlers: list[Handler]):
        self.handlers = self.handlers + handlers

    def add_tools(self, tools: list[Tool]):
        self.tools = self.tools + tools

    def add_instructions(self, instructions: list[str]):
        self.instructions = self.instructions + instructions

    def get_events(self, limit: Optional[int] = None) -> list[Event]:
        events = self.flow.get_events(limit=limit or 100)
        return events

    def compile_prompt(self, agent: Agent) -> str:
        from controlflow.orchestration.prompt_templates import (
            InstructionsTemplate,
            TasksTemplate,
            ToolTemplate,
        )

        agents = self.agents
        if agent not in agents:
            agents = agents + [agent]

        prompts = [
            *[agent.get_prompt(context=self) for agent in reversed(agents)],
            self.flow.get_prompt(context=self),
            TasksTemplate(tasks=self.tasks, context=self).render(),
            ToolTemplate(tools=self.tools, context=self).render(),
            InstructionsTemplate(instructions=self.instructions, context=self).render(),
        ]
        return "\n\n".join([p for p in prompts if p])

    def compile_messages(self, agent: Agent) -> list[BaseMessage]:
        events = self.get_events()
        compiler = MessageCompiler(
            events=events,
            llm_rules=agent.get_llm_rules(),
            system_prompt=self.compile_prompt(agent=agent),
        )
        messages = compiler.compile_to_messages(agent=agent)
        return messages

    def __enter__(self):
        self._context = ExitStack()
        self._context.enter_context(ctx(agent_context=self))
        return self

    def __exit__(self, *exc_info):
        self._context.close()
        return False


def get_context() -> Optional[AgentContext]:
    return ctx.get("agent_context")


def provide_agent_context(fn: Callable = None, *, context_kwarg: str = None):
    if fn is None:
        return partial(provide_agent_context, context_kwarg=context_kwarg)

    context_kwarg = context_kwarg or "context"

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if context_kwarg not in kwargs:
            if context := get_context():
                kwargs[context_kwarg] = context
        return fn(*args, **kwargs)

    return wrapper
