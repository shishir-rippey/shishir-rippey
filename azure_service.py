from utility.utils import list_files, run_in_thread, dump_json, flatten_json,json_to_excel
from loguru import logger 
import requests
from settings import settings


def file_upload(file): #azure
    url="https://api.qa.rippey.ai/appserver-api/analytics/general/file/signUrl"
    logger.info(f"Getting text extraction for {file}")
    response=requests.post(url=url, files={"file": open(file, "rb")})
    if response.ok:
        file_link_data=response.json()
    return file_link_data


def file_data_extraction(args): #azure
    url = "https://api.qa.rippey.ai/azure-extraction/extract/page_text"
    file_name,file_url = args
    payload = {
        "files": [
            {
        "file_url":file_url,
        "file_name": file_name
    }
        ]
    }
    print(payload)
    response = requests.post(url=url, json=payload, headers={"Cookie": settings.COOKIE})
    logger.info(response)
    if response.ok:
        result = response.json()
    return result


def extraction_from_task(args):#azure
    results, task_name = args
    azure_results=[]
    for result in results:
        page_text=result['page_texts']
        file_name = result['file_name']
        # url="http://localhost:8007/api/extraction_from_task"
        # url="https://api.qa.rippey.ai/azure-extraction/api/extraction_from_task"
        url ="https://api.qa.rippey.ai/entity-extract-ai/api/extraction_from_task"

        payload = {
            'user_input':page_text,
            'task_name':task_name,
            'file_name': file_name
        }
        # print(payload)
        response = requests.post(url=url, json=payload, headers={"Cookie": settings.COOKIE})
        print(response)
        logger.info(response)
        if response.ok:
            result = response.json()
            result['file_name'] = file_name
        return result







