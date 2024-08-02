import requests
from settings import settings
from loguru import logger

def get_text_extraction(file):
    url = "http://universal-parser-service.preprod.svc.cluster.local/upload/"
    logger.info(f"Getting text extraction for {file}")
    response = requests.post(url=url, files={"file": open(file, "rb")})
    if response.ok:
        result = response.json()
    return {
        "filename": file,
        "response": result
    }

def get_model_extraction(args):
    url = "https://api.qa.rippey.ai/entity-extract-ai/api/extraction_from_task"
    filename, extracted_text, task_name, operation_id, instance_id = args
    payload = {
        "user_input": [extracted_text],
        "task_name": task_name,
        "operation_id": operation_id,
        "instance_id": instance_id,
    }
    response = requests.post(url=url, json=payload, headers={"Cookie": settings.COOKIE})
    logger.info(response)
    if response.ok:
        result = response.json()
    return {
        "file_name": filename,
        "response": result
    }
