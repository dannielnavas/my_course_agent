from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.agents.support.state import State
from src.agents.support.nodes.conversation.node import conversation
from src.agents.support.nodes.extractor.node import extractor
from src.agents.support.nodes.booking.node import booking_node
from src.agents.support.routes.intent.route import intent_route

# from langgraph.checkpoint.postgres import PostgresSaver


def make_graph(config: TypedDict):
    checkpointer = config.get("checkpointer", None)
    builder = StateGraph(State)
    builder.add_node("conversation", conversation)
    builder.add_node("extractor", extractor)
    builder.add_node("booking", booking_node)

    builder.add_edge(START, "extractor")
    builder.add_conditional_edges("extractor", intent_route)
    builder.add_edge("conversation", END)
    builder.add_edge("booking", END)

    return builder.compile(checkpointer=checkpointer)

# with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
#     agent = builder.compile(checkpointer=checkpointer)
