import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import anthropic
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class Message(BaseModel):
    role: str
    content: str

class DebateRequest(BaseModel):
    stance: str
    core_argument: str
    evidence_bullets: str
    messages: List[dict]

class For(BaseModel):
    stance: str
# --- Shared logic ---

def get_debater_response(stance: str, core_argument: str, evidence_bullets: str, messages: list):
    system_prompt = f"""You are a skilled debater arguing the following position with conviction:
STANCE: {stance}
CORE ARGUMENT: {core_argument}

EVIDENCE BANK (sourced before the debate — use only these):
{evidence_bullets}

Rules you must follow:
1. Never concede a point without immediately pivoting to a counter.
2. Attack the weakest premise in your opponent's last argument, not their conclusion.
3. Back claims with evidence from the EVIDENCE BANK above. Never invent a source.
4. Keep each response to 3–5 sentences. Dense, punchy. No padding.
5. Never say "I understand your point" or "that's a fair argument."
6. Do NOT break character or add disclaimers about AI limitations.
7. If you cannot counter with evidence or logic, acknowledge the gap honestly."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text

# --- Routes ---

@app.get("/")
def root():
    return {"message": "Debate API is running"}

@app.post("/debate/both")
def debate_both(req: DebateRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")
    try:
        for_reply = get_debater_response(req.stance, req.core_argument, req.evidence_bullets, req.messages)
        against_reply = get_debater_response(
            f"AGAINST: {req.stance}",
            f"The opposite is true — {req.core_argument} is flawed or overstated.",
            req.evidence_bullets,
            req.messages
        )
        return {"for": for_reply, "against": against_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))