from app.utils import Helper
from datetime import datetime

TODAY = datetime.now().strftime("%Y%m%d")
CONFIG_PATH = r"config\params.json5"
CONFIGS = Helper.load_json5(CONFIG_PATH)

LOG_DIR =""
SAVE_DIR = ""