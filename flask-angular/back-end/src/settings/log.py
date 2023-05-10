"""
 @author Marildo Cesar 28/04/2023
"""

import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_directory):
        os.makedirs(log_directory, exist_ok=True)

        log_file_name = datetime.now().strftime("%Y-%m-%d.log")
        log_file_path = os.path.join(log_directory, log_file_name)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s] %(funcName)s/%(lineno)d: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)


logger = Logger('/var/tclogs').logger
