import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
LOG_DIR = "logs/gui"
os.makedirs(LOG_DIR, exist_ok=True)

# Log filename with date
log_file = os.path.join(LOG_DIR, f"gui_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Logger setup
logger = logging.getLogger("GUI_Logger")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console / GUI handler (if needed)
def gui_log(log_widget, level, message):
    """Log message to GUI widget and file"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    text = f"{timestamp} | {level} | {message}"
    
    # Append to GUI Text widget
    log_widget.insert("end", text + "\n")
    log_widget.see("end")
    
    # Log to file
    if level == "INFO":
        logger.info(message)
    elif level == "SUCCESS":
        logger.info("SUCCESS: " + message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)