import json
from settings import settings
from utility.utils import (
    dump_json,
    flatten_json,
    json_to_excel,
    list_files,
    run_in_thread,
    
)
from config import *
from local_service import get_text_extraction, get_model_extraction
from azure_service import file_upload, file_data_extraction, extraction_from_task
if __name__ == "__main__":
    files_in_dir =list_files(DATA_DIR, ALLOWED_EXTENSIONS)
    extraction_service = input("Enter extraction service (universal/azure): ").lower()
    if extraction_service == "azure":
        upload_results = run_in_thread(func=file_upload, iterables=files_in_dir)
        dump_json(settings.FILE_DATA_EXTRACTION,upload_results)
        upload_results = run_in_thread(func=file_data_extraction,iterables=[(result["data"]["file_name"], result["data"]["file_url"])
            for result in upload_results
        ],)
        dump_json(settings.EXTRACT_PAGE_TEXT, upload_results)
        upload_results = run_in_thread(func=extraction_from_task,iterables=[(result["result"], TASK_NAME) for result in upload_results
        ])
        dump_json(settings.AZURE_EXTRACTION, upload_results)
        azure_results= json.load(open("tmp/azure_extraction.json"))
        flat_azure_results=[]
        for results in azure_results:
            flat_json=flatten_json(results)
            flat_azure_results.append(flat_json)
        dump_json(settings.FLAT_AZURE_EXTRACTION, flat_azure_results)
#for local servive 
    elif extraction_service == "universal":
        results = run_in_thread(func=get_text_extraction, iterables=files_in_dir) #comment out for azure
        dump_json(settings.TEXT_EXTRACTION, results) #comment out for azure
        results = run_in_thread(
        func=get_model_extraction,
        iterables=[
            (result["filename"], result["response"]["data"][0]["extracted_text"], TASK_NAME, OPERATION_ID, INSTANCE_ID)
            for result in results
        ],)
        dump_json(settings.MODEL_EXTRACTION, results) #comment out for azure
        results = json.load(open("tmp/model_extraction.json"))
        flat_results = []
        for result in results:
            
            flat_json = flatten_json(result["response"])
            flat_json.update({
                "file_name": result["file_name"],
               "model_extraction": json.dumps(result, indent=2)
           })
            flat_results.append(flat_json)
            dump_json(settings.FLAT_MODEL_EXTRACTION, flat_results)
            json_to_excel(flat_results)
