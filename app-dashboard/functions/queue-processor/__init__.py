import logging
import azure.functions as func
def main(msg: func.QueueMessage):
    logging.info('Processing message: %s', msg.get_body().decode())
    # Normalize event, apply rules, write processed record to Table Storage
