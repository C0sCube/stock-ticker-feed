import os, zipfile, traceback
from app.logger import get_logger
# import pprint

logger = get_logger()

def zip_folder(folder_path, zip_path):
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
        