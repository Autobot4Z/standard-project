import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "INFO")

project_path = Path(__file__).resolve().parent
