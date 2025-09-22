from datetime import datetime
import os, traceback, time, zipfile
from app.market_parser import SplitMarketDataParser
from app.logger import get_logger
from app.utils import Helper
from app.constants import INPUT_PATH, OUTPUT_DIR,ZIP_DIR, ZIP_FILE_NAME

today_date = datetime.now().strftime("%d-%m-%Y")

def run():
    logger = get_logger()
    
    folder_path = Helper.create_dir(INPUT_PATH,today_date)
    output_path = Helper.create_dir(OUTPUT_DIR, today_date)
    zip_path = os.path.join(ZIP_DIR,f"{ZIP_FILE_NAME}_{today_date}.zip")
    
    logger.info(f"Program Has Started. {datetime.now()}")
    time.sleep(5)
    
    # logger.info(f"Output directory created: {output_path}")
    # logger.info(f"Zip directory created: {zip_path}")
    data_files = sorted_rate_files(folder_path)
    if not data_files:
        logger.warning(f"Folder: {folder_path} has no files attached.")
    

    parser = SplitMarketDataParser(output_path=output_path, exchange="NSE")
    
    src_total_tick_count = 0
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
                    logger.debug(traceback.format_exc())
            src_total_tick_count += len(lines)
            logger.info(f"Completed: {file_name} | Ticks: {len(lines)} | Total: {src_total_tick_count}")
        except Exception as e:
            logger.error(f"Runtime Error in {file_name}: {type(e).__name__}: {e}")
            logger.debug(traceback.format_exc())

    try:
        parser.flush_all_data()
        zip_folder(output_path,zip_path)
    except Exception as e:
        logger.error(f"Post Files Parsing: {type(e).__name__}: {e}")
        logger.debug(traceback.format_exc())
    
    logger.info(f"Program Has Ended. {datetime.now()}")

def sorted_rate_files(path):
    files = os.listdir(path)
    rate_files = [f for f in files if f.endswith(".txt")]
    rate_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    return rate_files

def zip_folder(folder_path, zip_path):
    logger = get_logger()
    logger.info(f"Zipping folder: {folder_path} into {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
                    file_count += 1
            logger.info(f"Zipping completed. {file_count} files added.")
    except Exception as e:
        logger.error(f"Zipping Error: {type(e).__name__}: {e}")
        logger.debug(traceback.format_exc())
