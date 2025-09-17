import os
from datetime import datetime
from app.utils import Helper

root_dir = os.path.dirname(os.path.dirname(__file__))
conf_path = os.path.join(root_dir, "config", "params.json5")
json_path = os.path.join(root_dir,"paths.json5")
CONFIG = Helper.load_json5(conf_path)
PATHS = Helper.load_json5(json_path)


TODAY = datetime.now().strftime("%Y%m%d")
# "NSE/2025/TICK/MAY_2025/GFDLCM_STOCK_TICK_19052025/RIIL.NSE.csv"
today = datetime.today()
year = today.strftime("%Y")
month = today.strftime("%B").upper()
day_str = today.strftime("%d%m%Y")


INPUT_PATH = PATHS["input_path"]
LOG_DIR = Helper.create_dir(PATHS["output_path"],"logs")
OUTPUT_DIR = Helper.create_dir(PATHS["output_path"],"data",TODAY)
