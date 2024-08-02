
import os
from pathlib import Path

from decouple import config


class Settings:
    COOKIE = config("ACCESS_TOKEN", default="access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3MDUwMzY2NDcsImV4cCI6MTczNjU3MjY0OSwiYXVkIjoiIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.a2hT4lI2Ux6XQLxx9Ry02K38JKOweuJQirRVvCKgt-c")

    TEMP_PATH = Path("tmp/")
    S3_UPLOADS = TEMP_PATH / "uploads.json"
    STATUS_RESPONSE = TEMP_PATH / "status.json"
    TEXT_EXTRACTION = TEMP_PATH / "text_extraction.json"
    FILE_DATA_EXTRACTION= TEMP_PATH / "file_data_extraction.json"
    
    MODEL_EXTRACTION = TEMP_PATH / "model_extraction.json"
    AZURE_EXTRACTION = TEMP_PATH / "azure_extraction.json"

    EXTRACT_PAGE_TEXT = TEMP_PATH / "extract_page_text.json"
    FLAT_MODEL_EXTRACTION = TEMP_PATH / "flat_model_extraction.json"
    FLAT_AZURE_EXTRACTION = TEMP_PATH / "flat_azure_extraction.json"


    def __init__(self):
        if not os.path.exists(self.TEMP_PATH):
            os.makedirs(self.TEMP_PATH)


settings = Settings()
