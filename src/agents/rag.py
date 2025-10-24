from pydantic import BaseModel, Field
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
    phone_number: str
    age: str


class ContactInfo(BaseModel):
    """ Contact information for a person """
    name: str = Field(description="The name of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")


llm_whith_structured_output = llm.with_structured_output(schema=ContactInfo)


def extractor(state: State):
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    history = state["messages"]
    if customer_name is None or len(history) >= 10:
        schema = llm_whith_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone_number"] = schema.phone
        new_state["age"] = schema.age
    return new_state


def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    system_message = f"You are a helpful assistant that can answer questions about the customer {state.get('customer_name', 'unknown')}"
    ai_message = llm.invoke(
        [('system', system_message), ('user', last_message.text)])
    new_state["messages"] = [ai_message]
    return new_state


builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge('extractor', "conversation")
builder.add_edge('conversation', END)

agent = builder.compile()
