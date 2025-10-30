from typing import Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from src.agents.support.routes.intent.propmt import SYSTEM_PROMPT
from src.agents.support.state import State


class RouteIntent(BaseModel):
    """Contact information for a person"""
    step: Literal["conversation", "booking"] = Field(
        'conversation', description="The next step in the routing process. conversation or booking")


llm = init_chat_model(
    "gpt-4o-mini",
    temperature=1,
)

llm = llm.with_structured_output(schema=RouteIntent)


def intent_route(state: State) -> Literal["conversation", "booking"]:
    history = state["messages"]
    schema = llm.invoke([('system', SYSTEM_PROMPT)] + history)
    if schema.step is not None:
        return schema.step
    else:
        return "conversation"
