from ftplib import FTP
import os, traceback
from app.constants import FTP_CONFIG
from app.logger import get_logger

logger = get_logger()

def ftp_file_transfer(file_path):
    
    if not os.path.exists(file_path):
        logger.error(f"Unable to ftp file path not found.")
        logger.debug(f"{file_path}")
        logger.debug(traceback.format_exc())
        return
    try:
        host = FTP_CONFIG["host"]
        username = FTP_CONFIG["username"]
        password = FTP_CONFIG["password"]
        output_path = FTP_CONFIG["file_path"]
    
    except Exception as e:
        logger.error(f"Unable to ftp as config error. Try checking, Returning without executing ftp")
        logger.error(traceback.format_exc())
        return
    
    try:
        logger.info("Beginning FTP.")
        with FTP(host) as ftp:
            ftp.login(user=username, passwd=password)
            with open(file_path, 'rb') as f:
                ftp.storbinary(f'STOR {output_path}', f)
            logger.info(f"Uploaded {file_path} as {output_path}")
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        logger.error(traceback.format_exc())