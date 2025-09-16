import logging
import os
import sys
from datetime import datetime

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


TRACE_LEVEL_NUM = 15
SAVE_LEVEL_NUM = 22
NOTICE_LEVEL_NUM = 25
MAX_LOG_SIZE = 1024 * 1024  # 1MB
DEFAULT_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_COLORS = {
    "TRAC": "white",
    "SAVE": "blue",
    "NOTI": "bold_cyan",
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

def _get_log_file(log_dir, base_name):
    today = datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join(log_dir, today)
    os.makedirs(folder_path, exist_ok=True)

    index = 0
    while True:
        file_path = os.path.join(folder_path, f"{base_name}_{index}.log")
        if not os.path.exists(file_path) or os.path.getsize(file_path) < MAX_LOG_SIZE:
            return file_path
        index += 1

class RotatingFileHandler(logging.FileHandler):
    """Custom file handler that checks size before every emit and rotates."""

    def __init__(self, log_dir, base_name, *args, **kwargs):
        self.log_dir = log_dir
        self.base_name = base_name
        file_path = _get_log_file(log_dir, base_name)
        super().__init__(file_path, *args, **kwargs)

    def emit(self, record):
        
        if os.path.exists(self.baseFilename) and os.path.getsize(self.baseFilename) >= MAX_LOG_SIZE:
            self.close()
            new_path = _get_log_file(self.log_dir, self.base_name)
            self.baseFilename = new_path
            self.stream = self._open()
        super().emit(record)

# --- Log Levels Quick Ref ---
# CRITICAL=50 | fatal error (bold red)
# ERROR   =40 | serious issue (red)
# WARNING =30 | non-fatal warning (yellow)
# NOTICE  =25 | milestones (cyan) *
# SAVE    =22 | saving data (blue) *
# INFO    =20 | runtime info (green)
# TRACE   =15 | fine debug (white) *
# DEBUG   =10 | dev details (cyan)
# (* = custom levels)

def setup_logger(name="daily_log",log_dir="logs",log_level=10,to_console=True,use_color=True, console_level = 15):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- File handler (no colors) ---
    file_handler = RotatingFileHandler(log_dir, name, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT, DATE_FORMAT))
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # --- Console handler (with color if available) ---
    if to_console:
        if use_color and COLORLOG_AVAILABLE:
            console_handler = colorlog.StreamHandler(sys.stdout)
            console_formatter = colorlog.ColoredFormatter(
                "%(log_color)s" + DEFAULT_FORMAT,
                datefmt=DATE_FORMAT,
                log_colors=LOG_COLORS,
            )
            console_handler.setFormatter(console_formatter)
        else:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT, DATE_FORMAT))

        console_handler.setLevel(console_level)
        logger.addHandler(console_handler)

    return logger


logging.addLevelName(TRACE_LEVEL_NUM, "TRAC")
logging.addLevelName(SAVE_LEVEL_NUM, "SAVE")
logging.addLevelName(NOTICE_LEVEL_NUM, "NOTI")


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kwargs)


def save(self, message, *args, **kwargs):
    if self.isEnabledFor(SAVE_LEVEL_NUM):
        self._log(SAVE_LEVEL_NUM, message, args, **kwargs)


def notice(self, message, *args, **kwargs):
    if self.isEnabledFor(NOTICE_LEVEL_NUM):
        self._log(NOTICE_LEVEL_NUM, message, args, **kwargs)


logging.Logger.trace = trace
logging.Logger.save = save
logging.Logger.notice = notice

#global it
_active_logger = None

def set_logger(logger):
    global _active_logger
    _active_logger = logger

def get_logger():
    return _active_logger or logging.getLogger("default_logger")