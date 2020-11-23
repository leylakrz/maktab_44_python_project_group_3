# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    filemode='w',
                    force=True)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
