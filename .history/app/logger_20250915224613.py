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


DEFAULT_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_COLORS = {
    'TRAC': 'white',
    'SAVE': 'blue',
    'NOTI': 'bold_cyan',
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARN': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

def _get_formatter(use_color=False):
    if use_color and COLORLOG_AVAILABLE:
        return colorlog.ColoredFormatter(
            "%(log_color)s" + DEFAULT_FORMAT,
            datefmt=DATE_FORMAT,
            log_colors=LOG_COLORS
        )
    return logging.Formatter(DEFAULT_FORMAT, datefmt=DATE_FORMAT)

def _add_console_handler(logger, level, use_color=True):
    handler = (
        colorlog.StreamHandler(sys.stdout)
        if use_color and COLORLOG_AVAILABLE
        else logging.StreamHandler(sys.stdout)
    )
    handler.setFormatter(_get_formatter(use_color))
    handler.setLevel(level)
    logger.addHandler(handler)


def setup_logger(
    name="MarketLogger",
    log_dir="logs",
    log_level=logging.DEBUG,
    to_console=True,
    to_file=True,
    use_color=True
):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)
    logger.propagate = False

    if to_file:
        # timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        today = datetime.now().strftime("%Y%m%d")
        folder_path = os.path.join(log_dir,today)
        os.makedirs(folder_path, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setFormatter(_get_formatter(use_color=False))
        file_handler.setLevel(TRACE_LEVEL_NUM)
        logger.addHandler(file_handler)

    if to_console:
        _add_console_handler(logger, log_level, use_color)

    return logger


# --- Global registry with short names ---
_active_logger = None

def set_logger(logger):
    global _active_logger
    _active_logger = logger

def get_logger():
    return _active_logger or logging.getLogger("default_logger")
