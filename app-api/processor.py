# app-api/app/processor.py
import os
import json
import logging
from datetime import datetime
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobServiceClient, ContentSettings

logger = logging.getLogger(__name__)

# ENV variables expected:
#  - AZURE_STORAGE_CONNECTION_STRING  (or use individual account credentials)
#  - RAW_EVENTS_CONTAINER   (default: raw-events)
#  - EVENTS_QUEUE_NAME      (default: events-queue)

RAW_CONTAINER = os.getenv("RAW_EVENTS_CONTAINER", "raw-events")
QUEUE_NAME = os.getenv("EVENTS_QUEUE_NAME", "events-queue")
STORAGE_CONN = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not STORAGE_CONN:
    logger.warning("AZURE_STORAGE_CONNECTION_STRING not set. Local development may fail.")

def get_blob_client():
    if not STORAGE_CONN:
        raise ValueError("Missing AZURE_STORAGE_CONNECTION_STRING")
    return BlobServiceClient.from_connection_string(STORAGE_CONN)

def get_queue_client():
    if not STORAGE_CONN:
        raise ValueError("Missing AZURE_STORAGE_CONNECTION_STRING")
    return QueueClient.from_connection_string(STORAGE_CONN, QUEUE_NAME)

def save_raw_event(event: dict, prefix: str = "event"):
    """
    Save the raw event JSON to blob storage with a timestamped key.
    Returns the blob path.
    """
    try:
        client = get_blob_client()
        container_client = client.get_container_client(RAW_CONTAINER)
        # create container if not exists
        try:
            container_client.create_container()
        except Exception:
            pass

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        blob_name = f"{prefix}/{timestamp}_{event.get('id','') or ''}.json"
        content = json.dumps(event, default=str).encode("utf-8")
        content_settings = ContentSettings(content_type="application/json")
        container_client.upload_blob(name=blob_name, data=content, overwrite=True, content_settings=content_settings)

        logger.info("Saved raw event to blob: %s", blob_name)
        return blob_name
    except Exception as e:
        logger.exception("Failed to save raw event: %s", e)
        raise

def enqueue_event(message: dict):
    """
    Push a message to the storage queue for background processing.
    """
    try:
        qc = get_queue_client()
        # message must be a string
        payload = json.dumps(message, default=str)
        qc.send_message(payload)
        logger.info("Enqueued event to queue '%s'", QUEUE_NAME)
        return True
    except Exception as e:
        logger.exception("Failed to enqueue event: %s", e)
        raise

def normalize_event(raw: dict) -> dict:
    """
    Basic normalization example: unify keys and attach metadata.
    Extend this for your domain-specific normalization.
    """
    normalized = {
        "id": raw.get("id") or raw.get("eventId") or None,
        "source": raw.get("source", "unknown"),
        "type": raw.get("type", "unknown"),
        "payload": raw.get("payload", raw.get("data", raw)),
        "received_at": datetime.utcnow().isoformat() + "Z"
    }
    # Add simple derived field example
    if isinstance(normalized["payload"], dict) and normalized["payload"].get("severity"):
        normalized["severity"] = normalized["payload"].get("severity")
    else:
        normalized["severity"] = "info"
    return normalized
