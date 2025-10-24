from langgraph.graph import StateGraph, START, END

from src.agents.support.state import State
from src.agents.support.nodes.conversation.node import conversation
from src.agents.support.nodes.extractor.node import extractor

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge('extractor', "conversation")
builder.add_edge('conversation', END)

agent = builder.compile()
