from langgraph.graph import StateGraph, START, END
import random
from typing import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model


llm = init_chat_model(
    "gpt-4o-mini",
    temperature=1,
)
openai_vector_store_ids = [
    "vs_68fa19c8385881918734a172b75bd5ff"
]

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids,
}

llm = llm.bind_tools([file_search_tool])


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
    last_message = history[-1]
    ai_message = llm.invoke(last_message.text)
    new_state["messages"] = [ai_message]
    return new_state


builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge('node_1', END)

agent = builder.compile()
