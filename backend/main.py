from fastapi import FastAPI
import agent
from pydantic import BaseModel
from typing import Literal

# Message list JSON fields
class Message(BaseModel):
    speaker: Literal["for", "against"]
    message: str

# Main item JSON fields
class Item(BaseModel):
    topic: str
    speaker: float
    conversation: list[Message]

# Setup app
app = FastAPI()

# Add listener for message POST request
@app.post("/message/")
def create_item(item: str):
    # Process the received item data
    debate_data = agent.decode_json(item)

    # Run AI Algorithm
    response_message = agent.chat(debate_data)

    # Return output
    return {"message": response_message}