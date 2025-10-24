from langgraph.graph import MessagesState


class State(MessagesState):
    customer_name: str
    phone_number: str
    age: str
