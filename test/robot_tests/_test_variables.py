import os
from pathlib import Path

BROWSER = os.environ.get("BROWSER").lower() if os.environ.get("BROWSER") else "headlesschrome"
# BROWSER = os.environ.get("BROWSER").lower() if os.environ.get("BROWSER") else "chrome"

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
URL = "http://localhost:8000/apps/edit"
