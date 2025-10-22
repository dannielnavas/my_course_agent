from langgraph.graph import StateGraph, START, END
import random
from typing import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model


llm_generic = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    temperature=1,
)


class State(MessagesState):
    customer_name: str
    my_age: int


def node_1(state: State):
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "Danniel Navas"
    else:
        new_state["my_age"] = random.randint(18, 35)
    history = state["messages"]
    ai_message = llm_generic.invoke(history)
    new_state["messages"] = [ai_message]
    return new_state


builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge('node_1', END)

agent = builder.compile()
