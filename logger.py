import logging
import os

'''logger.debug("This is a debug message")
logger.info("Informational message")
logger.warning("A warning message")
logger.error("An error has occurred")
logger.critical("Critical issue!")'''


# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create a logger
logger = logging.getLogger('my_app_logger')
logger.setLevel(logging.DEBUG)  # Log all levels DEBUG and above

# Create file handler to write logs to file
file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.DEBUG)

# Create console handler (optional) to also print logs to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
