from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from src.agents.support.state import State
from src.agents.support.nodes.extractor.propmt import SYSTEM_PROMPT


class ContactInfo(BaseModel):
    """ Contact information for a person """
    name: str = Field(description="The name of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")


llm = init_chat_model(
    "gpt-4o-mini",
    temperature=1,
)

llm = llm.with_structured_output(schema=ContactInfo)


def extractor(state: State):
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    history = state["messages"]
    if customer_name is None or len(history) >= 10:
        schema = llm.invoke([('system', SYSTEM_PROMPT)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone_number"] = schema.phone
        new_state["age"] = schema.age
    return new_state
