from fastapi import FastAPI
import agent
from pydantic import BaseModel
from typing import Literal

class Message(BaseModel):
    speaker: Literal["for", "against"]
    message: str

class Item(BaseModel):
    topic: str
    speaker: float
    conversation: list[Message]


app = FastAPI()

@app.post("/message/")
def create_item(item: str):
    # Process the received item data
    item_data = agent.decode_json(item)
    print(f"Received item: {item_data.get("topic")}")

    # Run AI Algorithm
    # ... TODO
    
    response_message = "placeholder"

    # Return output
    return {"message": response_message}