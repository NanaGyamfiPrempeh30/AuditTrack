import logging
import json
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.data.tables import TableServiceClient, TableClient
import azure.functions as func

from app_api_processor import processor  # we will provide a small shim below

logger = logging.getLogger("queue-processor")
logger.setLevel(logging.INFO)

# Environment variables expected:
# AZURE_STORAGE_CONNECTION_STRING
# PROCESSED_CONTAINER (default: processed-events)
# PROCESSED_TABLE (default: processedEvents)

PROCESSED_CONTAINER = os.getenv("PROCESSED_CONTAINER", "processed-events")
PROCESSED_TABLE = os.getenv("PROCESSED_TABLE", "processedEvents")
STORAGE_CONN = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


def write_processed_blob(blob_name: str, data: dict):
    client = BlobServiceClient.from_connection_string(STORAGE_CONN)
    container = client.get_container_client(PROCESSED_CONTAINER)
    try:
        container.create_container()
    except Exception:
        pass
    content = json.dumps(data, default=str).encode("utf-8")
    container.upload_blob(name=blob_name, data=content, overwrite=True, content_settings=ContentSettings(content_type="application/json"))
    logger.info("Wrote processed blob: %s", blob_name)

def write_table_record(item: dict):
    # Use Tables for small metadata queries
    svc = TableServiceClient.from_connection_string(STORAGE_CONN)
    try:
        table = svc.create_table_if_not_exists(table_name=PROCESSED_TABLE)
    except Exception:
        table = svc.get_table_client(PROCESSED_TABLE)
    # PartitionKey & RowKey required
    record = {
        "PartitionKey": item.get("source", "unknown"),
        "RowKey": item.get("id") or item.get("eventId") or item.get("received_at"),
        **{k: str(v) for k, v in item.items() if k not in ("source", "id", "received_at")}
    }
    table_client = svc.get_table_client(PROCESSED_TABLE)
    table_client.upsert_entity(entity=record, mode="merge")
    logger.info("Wrote table record for event %s", record.get("RowKey"))


def main(msg: func.QueueMessage):
    body = msg.get_body().decode('utf-8')
    logger.info("Queue trigger received message")
    try:
        raw = json.loads(body)
    except Exception as e:
        logger.exception("Failed to parse message JSON: %s", e)
        return

    # Normalize using the processor.normalize_event
    normalized = processor.normalize_event(raw)
    # A sample rule: mark high severity if payload contains 'error' or severity == 'high'
    severity = normalized.get("severity", "info")
    payload_text = json.dumps(normalized.get("payload", {})).lower()
    if severity.lower() == "high" or "error" in payload_text:
        normalized["alert"] = True
    else:
        normalized["alert"] = False

    # Save processed data
    ts = normalized.get("received_at", "unknown").replace(":", "-")
    blob_name = f"processed/{normalized.get('id','')}_{ts}.json"
    try:
        write_processed_blob(blob_name, normalized)
        write_table_record(normalized)
    except Exception:
        logger.exception("Failed to persist processed event")
        return

    logger.info("Processed event %s (alert=%s)", normalized.get("id"), normalized.get("alert"))
