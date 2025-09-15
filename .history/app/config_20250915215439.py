import os
from datetime import datetime
from app.utils import Helper

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load main params
CONFIG_PATH = os.path.join(BASE_DIR, "config", "params.json5")
CONFIG = Helper.load_json(CONFIG_PATH, typ="json5")

# Derived paths
TODAY = datetime.now().strftime("%Y%m%d")
LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", TODAY)
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Auto-create important dirs
Helper.create_dir(LOG_DIR)
Helper.create_dir(OUTPUT_DIR)
