import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Define the log file name with timestamp
LOG_FILE_NAME = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"

# Define the logs directory path
LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Define the full path for the log file
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE_NAME)

# Configure the logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define a rotating file handler for log rotation
handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,  # Keep 5 backup files
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter(
    "[ %(asctime)s ] %(levelname)s [%(name)s] - Line %(lineno)d - %(message)s"
))

# Add the handler to the logger
logger.addHandler(handler)


"""
if __name__=="__main__":
    logger.info("logging has started.")
"""