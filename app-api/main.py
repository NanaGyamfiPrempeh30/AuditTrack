from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import os
import logging

app = FastAPI(title="AuditTrack API")

class Event(BaseModel):
    source: str
    type: str
    payload: dict

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(event: Event):
    # Save raw event to blob (via SDK) or push to queue
    # For demo: return acknowledgement
    event_id = str(uuid4())
    logging.info(f"Received event {event_id} from {event.source}")
    # TODO: push to storage queue or blob
    return {"id": event_id, "status": "queued"}
