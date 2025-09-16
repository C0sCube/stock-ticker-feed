from datetime import datetime
import os, traceback, logging
from app.market_parser import SplitMarketDataParser
from app.logger import setup_logger
from app.utils import Helper
from app.constants import CONFIG, LOG_DIR

config = CONFIG

logger = setup_logger(name="market_data", log_dir=LOG_DIR)

folder_path = r"C:\Users\kaustubh.keny\Downloads\16-09-2025"

def sorted_rate_files(folder_path):
    files = os.listdir(folder_path)
    rate_files = [f for f in files if f.startswith("RealTime_")]
    rate_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    return rate_files

def run():
    logger.notice("Program Has Started.")
    parser = SplitMarketDataParser(config, logger, exchange="NSE")

    data_files = sorted_rate_files(folder_path)
    for file_name in data_files:
        file_path = os.path.join(folder_path, file_name)
        logger.info(f"Processing file: {file_name}")

        try:
            lines = Helper.read_file(file_path).splitlines()
            for line in lines:
                try:
                    parser.process_ticker(line)
                except Exception as e:
                    logger.error(f"Ticker error in {file_name}: {type(e).__name__}: {e}")
                    # logger.debug(traceback.format_exc())

            logger.info(f"Completed processing file: {file_name}")

        except Exception as e:
            logger.error(f"File error {file_name}: {type(e).__name__}: {e}")
            logger.debug(traceback.format_exc())

    # flush any leftover tick bins
    parser.flush_all_data()

    logger.notice("Program Has Ended.")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.warning("Simulation stopped by user")
    except Exception as e:
        logger.exception(f"Fatal error: {type(e).__name__}: {e}")


# import os, traceback
# from concurrent.futures import ThreadPoolExecutor, as_completed

# from app.market_parser import SplitMarketDataParser
# from app.logger import setup_logger
# from app.utils import Helper
# from app.constants import CONFIG, LOG_DIR

# logger = setup_logger(name="market_data", log_dir=LOG_DIR)
# folder_path = r"C:\Users\kaustubh.keny\Downloads\16-09-2025"

# def sorted_rate_files(folder_path):
#     files = os.listdir(folder_path)
#     rate_files = [f for f in files if f.startswith("RealTime_")]
#     rate_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
#     return rate_files

# def process_file(file_path, worker_id):
#     parser = SplitMarketDataParser(CONFIG, logger, exchange="NSE", worker_id=worker_id)
#     try:
#         lines = Helper.read_file(file_path).splitlines()
#         for line in lines:
#             try:
#                 parser.process_ticker(line)
#             except Exception as e:
#                 logger.error(f"Ticker error in {file_path}: {type(e).__name__}: {e}")
#                 logger.debug(traceback.format_exc())
#         return file_path, "ok"
#     except Exception as e:
#         return file_path, f"fail: {type(e).__name__}: {e}"
#     finally:
#         parser.flush_all_data()


# def main():
#     logger.notice("Program Started (Threaded Processing)")

#     data_files = sorted_rate_files(folder_path)

#     with ThreadPoolExecutor(max_workers=4) as executor:  # try 4 threads
#         futures = []
#         for i, file_name in enumerate(data_files):
#             file_path = os.path.join(folder_path, file_name)
#             futures.append(executor.submit(process_file, file_path, i % 4))

#         for fut in as_completed(futures):
#             fname, status = fut.result()
#             logger.notice(f"{fname}: {status}")

#     logger.notice("Program Ended")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         logger.warning("Simulation stopped by user")
#     except Exception as e:
#         logger.exception(f"Fatal error: {type(e).__name__}: {e}")
