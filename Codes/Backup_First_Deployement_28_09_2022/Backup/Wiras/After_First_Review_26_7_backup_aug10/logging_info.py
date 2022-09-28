"""
This file demonstrates the logging of data received from Azure,data send to Azure and the errors while executing the
code.
"""
import logging
import os
from general_configurations import BASE_DIR
from logging.handlers import RotatingFileHandler
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

class Datalogs(object):
    """
    This class consist of function which write the error logs to a file by specifying the filename and message to be
    written.
    """
    @classmethod
    def errorlog(cls, filename, level=logging.INFO):
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(lineno)d - %(levelname)s - %(message)s"
        )
        file_handler = RotatingFileHandler(
            os.path.join(BASE_DIR, 'Logs', filename),
            maxBytes=20000,
            mode="w",
            backupCount=2,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def logging_error(self, data, filename):
        logging_error = self.errorlog(filename)
        logging_error.info(data)
