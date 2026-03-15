import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import agent
import item

# Load .env from project root so it works when running from backend/
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
_cors_origins_list = [o.strip() for o in _cors_origins.split(",") if o.strip()]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/message/")
def create_item(item: item.Item):
    response_message = agent.chat(item)
    return {"message": response_message}
