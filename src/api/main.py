from langchain_core.messages import HumanMessage
from agents.support.agent import agent
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Message(BaseModel):
    message: str


@app.post("/chat/{chat_id}")
def chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)
    response = agent.invoke({"messages": [human_message]})
    last_message = response["messages"][-1]
    return last_message.text


@app.post("/chat/{chat_id}/stream")
async def stream_chat(chat_id: str, item: Message):
    human_message = HumanMessage(content=item.message)

    async def generate_response():
        for message_chunk, metadata in agent.stream({"messages": [human_message]}, stream_mode="messages"):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"
    return StreamingResponse(generate_response(), media_type="text/event-stream")
