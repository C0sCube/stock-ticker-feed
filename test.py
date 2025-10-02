from app.ftp_connector import ftp_file_transfer
from app.logger import setup_logger, set_logger
import logging
# Initialize scheduler logger
log_dir = r"C:\Users\kaustubh.keny\Projects\OUTPUTS\ticker-ops\logs"
logger = setup_logger(name="scheduler", log_dir=log_dir, console_level=logging.INFO)
set_logger(logger)
path = r"C:\Users\kaustubh.keny\Downloads\lookup.csv"

ftp_file_transfer(path)