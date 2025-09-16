import os
from datetime import datetime
from app.utils import Helper

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "params.json5")
CONFIG = Helper.load_json5(CONFIG_PATH)


TODAY = datetime.now().strftime("%Y%m%d")
# "NSE/2025/TICK/MAY_2025/GFDLCM_STOCK_TICK_19052025/RIIL.NSE.csv"
today = datetime.today()
year = today.strftime("%Y")
month = today.strftime("%B").upper()
day_str = today.strftime("%d%m%Y")
path = os.path.join(BASE_DIR, "NSE", year, "TICK", f"{month}_{year}", f"GFDLCM_STOCK_TICK_{day_str}")



output_dir = r"C:\Users\kaustubh.keny\Projects\OUTPUTS\ticker-output"

LOG_DIR = Helper.create_dir(output_dir,TODAY,"logs")
OUTPUT_DIR = Helper.create_dir(output_dir,TODAY,"data")
