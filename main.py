from datetime import datetime, timedelta
import time, traceback, logging
from runner import run
from app.constants import SCHEDULE_START_TIME, SCHEDULE_INTERVAL,LOG_DIR
from app.logger import setup_logger, set_logger

# Initialize scheduler logger
logger = setup_logger(name="scheduler", log_dir=LOG_DIR, console_level=logging.INFO)
set_logger(logger)  # Optional global logger setup

def wait_until_start(start_time):
    now = datetime.now()
    today_start = datetime.combine(now.date(), start_time)
    if now > today_start:
        today_start += timedelta(days=1)
    wait_seconds = (today_start - now).total_seconds()
    logger.info(f"Waiting {int(wait_seconds)} seconds until start at {today_start}")
    time.sleep(wait_seconds)

def schedule_loop():
    try:
        while True:
            logger.info(f"Triggering scheduled run at {datetime.now()}")
            start = datetime.now()
            try:
                run()
                duration = (datetime.now() - start).total_seconds()
                logger.info(f"Run completed in {duration:.2f} seconds")
                
            except Exception as e:
                logger.critical(f"Fatal error during run: {type(e).__name__}: {e}")
                logger.debug(traceback.format_exc())
                
            logger.info(f"Waiting {SCHEDULE_INTERVAL} seconds until next run...")
            time.sleep(SCHEDULE_INTERVAL)
            
    except KeyboardInterrupt:
        logger.warning(f"Scheduler interrupted by user at {datetime.now()}")
        
    except Exception as e:
        logger.critical(f"Unexpected error in scheduler loop: {type(e).__name__}: {e}")
        logger.debug(traceback.format_exc())

if __name__ == "__main__":
    logger.info(f"Scheduler initialized at {datetime.now()}")
    wait_until_start(SCHEDULE_START_TIME)
    schedule_loop()

# from datetime import datetime
# import os, traceback, logging, time
# from app.market_parser import SplitMarketDataParser
# from app.logger import setup_logger, set_logger
# from app.utils import Helper
# from app.constants import LOG_DIR, INPUT_PATH, OUTPUT_DIR

# folder_path = INPUT_PATH
# data_for = INPUT_PATH.split("\\")[-1]
# output_path = Helper.create_dir(OUTPUT_DIR,data_for)

# logger = setup_logger(name="market_data", log_dir=LOG_DIR, console_level=15)
# set_logger(logger) #made global not used tho !! passed as a parameter to the class

# def sorted_rate_files(path):
#     files = os.listdir(path)
#     rate_files = [f for f in files if f.startswith("RealTime_")]
#     rate_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
#     return rate_files

# def zip_files(path):
#     pass

# def run():
#     logger.info(f"Program Has Started. {datetime.now()}")
#     time.sleep(5)
#     parser = SplitMarketDataParser(
#         # logger=logger,
#         output_path=output_path,
#         exchange="NSE"
#     )

#     data_files = sorted_rate_files(folder_path)
    
#     src_total_tick_count = 0
    
#     for file_name in data_files:
#         file_path = os.path.join(folder_path, file_name)
#         logger.info(f"Processing file: {file_name}")

#         src_file_tick_count = 0
#         try:
#             lines = Helper.read_file(file_path).splitlines()
#             src_file_tick_count = len(lines)
#             for line in lines:
#                 try:
#                     parser.process_ticker(line)
#                 except Exception as e:
#                     logger.error(f"Ticker error in {file_name}: {type(e).__name__}: {e}")
#                     logger.debug(traceback.format_exc())
#             src_total_tick_count+=src_file_tick_count
#             logger.info(f"Completed Processing: {file_name} File Ticks:{src_file_tick_count}\tTotal Ticks so Far:{src_total_tick_count}")

#         except Exception as e:
#             logger.error(f"Function: run() File: {file_name} Error: {type(e).__name__}: {e}")
#             logger.debug(traceback.format_exc())

#     # flush any leftover tick bins
#     parser.flush_all_data()

#     logger.info(f"Program Has Ended. {datetime.now()}")

# if __name__ == "__main__":
#     try:
#         run()
#     except KeyboardInterrupt:
#         logger.warning("File: main.py -> Simulation stopped by user")
#         logger.debug(traceback.format_exc())
#     except Exception as e:
#         logger.critical(f"File: main.py -> Fatal error: {type(e).__name__}: {e}")
#         logger.debug(traceback.format_exc())


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
