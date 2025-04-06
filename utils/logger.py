import logging
from config import DEBUG_LEVEL

# Map string level names to logging constants
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Get the logging level constant, default to INFO if invalid
        level = LOG_LEVELS.get(DEBUG_LEVEL.upper(), logging.INFO)
        logger.setLevel(level)
    return logger