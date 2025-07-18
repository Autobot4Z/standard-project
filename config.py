import os
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import cloud_log

load_dotenv()

DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "INFO")
CLOUD_LOG_NAME = os.getenv("CLOUD_LOG_NAME")
CLOUD_ERROR_LOG_NAME = os.getenv("CLOUD_ERROR_LOG_NAME")
if not CLOUD_LOG_NAME or not CLOUD_ERROR_LOG_NAME:
    cloud_log("Umgebung: CLOUD_LOG_NAME und CLOUD_ERROR_LOG_NAME müssen gesetzt sein.")
    raise RuntimeError("Umgebung: CLOUD_LOG_NAME und CLOUD_ERROR_LOG_NAME müssen gesetzt sein.")

project_path = Path(__file__).resolve().parent

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
if not GOOGLE_CREDENTIALS_PATH:
    cloud_log("Umgebung: GOOGLE_CREDENTIALS_PATH muss gesetzt sein.")
    raise RuntimeError("Umgebung: GOOGLE_CREDENTIALS_PATH muss gesetzt sein.")

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
if not GOOGLE_CLOUD_PROJECT:
    cloud_log("Umgebung: GOOGLE_CLOUD_PROJECT muss gesetzt sein.")
    raise RuntimeError("Umgebung: GOOGLE_CLOUD_PROJECT muss gesetzt sein.")

IDEMPOTENCY_COLLECTION = os.getenv("IDEMPOTENCY_COLLECTION")
if not IDEMPOTENCY_COLLECTION:
    cloud_log("Umgebung: IDEMPOTENCY_COLLECTION muss gesetzt sein.")
    raise RuntimeError("Umgebung: IDEMPOTENCY_COLLECTION muss gesetzt sein.")
