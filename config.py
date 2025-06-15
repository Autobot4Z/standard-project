import os
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import log_error

load_dotenv()

DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "INFO")
CLOUD_LOG_NAME = os.getenv("CLOUD_LOG_NAME")
CLOUD_ERROR_LOG_NAME = os.getenv("CLOUD_ERROR_LOG_NAME")
if not CLOUD_LOG_NAME or not CLOUD_ERROR_LOG_NAME:
    log_error("Umgebung: CLOUD_LOG_NAME und CLOUD_ERROR_LOG_NAME müssen gesetzt sein.")
    raise RuntimeError("Umgebung: CLOUD_LOG_NAME und CLOUD_ERROR_LOG_NAME müssen gesetzt sein.")

project_path = Path(__file__).resolve().parent

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
if not GOOGLE_CREDENTIALS_PATH:
    log_error("Umgebung: GOOGLE_CREDENTIALS_PATH muss gesetzt sein.")
    raise RuntimeError("Umgebung: GOOGLE_CREDENTIALS_PATH muss gesetzt sein.")

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
if not GOOGLE_CLOUD_PROJECT:
    log_error("Umgebung: GOOGLE_CLOUD_PROJECT muss gesetzt sein.")
    raise RuntimeError("Umgebung: GOOGLE_CLOUD_PROJECT muss gesetzt sein.")

IDEMPOTENCY_COLLECTION = os.getenv("IDEMPOTENCY_COLLECTION")
if not IDEMPOTENCY_COLLECTION:
    log_error("Umgebung: IDEMPOTENCY_COLLECTION muss gesetzt sein.")
    raise RuntimeError("Umgebung: IDEMPOTENCY_COLLECTION muss gesetzt sein.")
