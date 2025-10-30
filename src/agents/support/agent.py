from langgraph.graph import StateGraph, START, END

from src.agents.support.state import State
from src.agents.support.nodes.conversation.node import conversation
from src.agents.support.nodes.extractor.node import extractor
from src.agents.support.nodes.booking.node import booking_node
from src.agents.support.routes.intent.route import intent_route

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)
builder.add_node("booking", booking_node)

builder.add_edge(START, "extractor")
builder.add_conditional_edges("extractor", intent_route)
builder.add_edge("conversation", END)
builder.add_edge("booking", END)


agent = builder.compile()
