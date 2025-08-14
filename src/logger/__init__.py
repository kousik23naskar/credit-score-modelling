import os
import sys
import logging
from datetime import datetime

# Directory and file setup
LOG_DIR = "logs"
# Creating the log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Generate the log file name based on the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

#LOG_FORMAT = "[ %(asctime)s ] %(lineno)d: %(module)s- %(levelname)s -  %(message)s"
# Define the detailed logging format string
LOG_FORMAT = (
    "[%(asctime)s] "       # Timestamp when the log message is created
    "[%(levelname)s] "     # Logging level (e.g., INFO, DEBUG, ERROR)
    "[File: %(filename)s] " # File name where the log call was made
    "[Line: %(lineno)d] "  # Line number in the source code where the log call was made
    #"[Module: %(module)s] "  # Module (filename) where the log call was made
    #"[Function: %(funcName)s] "  # Function name where the log call was made
    "- %(message)s"        # The actual log message
)


def setup_logger(name: str = "appLogger") -> logging.Logger:
    """
    Creates and returns a configured logger instance.

    Args:
        name (str): Name of the logger (Ex.: appLogger or creditscoreLogger).

    Returns:
        logging.Logger: A logger that writes to both file and console.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO) # Set the logging level to INFO/WARNING/ERROR

    # Avoid adding multiple handlers if logger already has them
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_PATH)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT)) # Set the custom logging format defined above


        # Console (stream) handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Optional: Prevent propagation to root logger
        logger.propagate = False

    return logger

# Optionally create a default logger instance for immediate use
logger = setup_logger()

# Example usage:
# from src.logger import setup_logger

# logger = setup_logger(__name__)  # You can use __name__ for per-module logging

# logger.info("App started")
# logger.error("Something went wrong")