from datetime import datetime
import random, time, traceback, os, logging

from app.market_parser import MarketDataParser, SplitMarketDataParser
from app.logger import setup_logger
from app.utils import Helper
from app.constants import CONFIG, LOG_DIR

config = CONFIG

logger = setup_logger(name="market_data", log_dir=LOG_DIR)
error_logger = setup_logger(name="error_log", log_dir=LOG_DIR, log_level=logging.ERROR, to_console=False)

folder_path = r"C:\Users\kaustubh.keny\Downloads\16-09-2025"

def sorted_rate_files(folder_path):
    files = os.listdir(folder_path)
    rate_files = [f for f in files if f.startswith("RealTime_")]
    rate_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    return rate_files

data_files = sorted_rate_files(folder_path)

try:
    logger.notice("Program Has Started.")
    parser = SplitMarketDataParser(config, logger, exchange="NSE")

    for file_name in data_files:
        try:
            file_path = os.path.join(folder_path, file_name)
            logger.info(f"Processing file: {file_name}")
            file_content = Helper.read_file(file_path)

            lines = file_content.splitlines()
            for line in lines:
                try:
                    parser.process_ticker(line)
                except Exception as e:
                    error_logger.error(f"Error processing ticker in file {file_name}: {type(e)}:{e}")
                    error_logger.debug(traceback.format_exc())

            logger.info(f"Completed processing file: {file_name}")

        except Exception as e:
            error_logger.error(f"Error processing file {file_name}: {type(e)}:{e}")
            error_logger.debug(traceback.format_exc())

    logger.notice("Program Has Ended.")
except Exception as e:
    error_logger.exception(f"{type(e)}:{e}")
    error_logger.debug(traceback.format_exc())
except KeyboardInterrupt:
    logger.warning("\nSimulation stopped.")