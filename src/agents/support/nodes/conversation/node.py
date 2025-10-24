from langchain.chat_models import init_chat_model
from src.agents.support.state import State
from src.agents.support.nodes.conversation.tools import tools
from src.agents.support.nodes.conversation.propmt import SYSTEM_PROMPT
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=1,
)

llm = llm.bind_tools(tools)


def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1]
    system_message = SYSTEM_PROMPT
    ai_message = llm.invoke(
        [('system', system_message), ('user', last_message.text)])
    new_state["messages"] = [ai_message]
    return new_state
