import os
from datetime import datetime, time
from app.utils import Helper

root_dir = os.path.dirname(os.path.dirname(__file__))
conf_path = os.path.join(root_dir, "config", "params.json")
json_path = os.path.join(root_dir,"paths.json")

CONFIG = Helper.load_json(conf_path)
PATHS = Helper.load_json(json_path)


TODAY = datetime.now().strftime("%Y-%m-%d")
# "NSE/2025/TICK/MAY_2025/GFDLCM_STOCK_TICK_19052025/RIIL.NSE.csv"
# today = datetime.today()
# year = today.strftime("%Y")
# month = today.strftime("%B").upper()
# day_str = today.strftime("%d%m%Y")


INPUT_PATH = PATHS["input_path"]
LOG_DIR = Helper.create_dir(PATHS["output_path"],"logs")
OUTPUT_DIR = Helper.create_dir(PATHS["output_path"],"data")
ZIP_DIR = Helper.create_dir(PATHS["output_path"],"zip")

ZIP_FILE_NAME = "NSE_TICK_CSV"


#Bin size to bin data
BIN_SIZE = 30
FILL_NA = "Nil"

#Scheduler Constants
raw_time = PATHS["start_time"]
start_hour,start_minute = int(raw_time[:2]), int(raw_time[2:4])
SCHEDULE_START_TIME = time(start_hour, start_minute)
SCHEDULE_INTERVAL = int(PATHS["interval_hours"]) * 3600


#Sql Constants
DB_CONFIG = CONFIG["DB_CONFIG_DEFAULT"]
SP_CONFIG = CONFIG["SP_CONFIGS"]["nse_symbol_mapper"]

#FTP Constants

FTP_CONFIG = CONFIG.get("FTP_CONFIG_DEFAULT",{})