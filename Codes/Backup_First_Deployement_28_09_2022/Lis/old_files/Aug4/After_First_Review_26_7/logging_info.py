"""
This file demonstrates the logging of data received from Azure,data send to Azure and the errors while executing the
code.
"""
import logging
import os
# from general_configurations import Error_Logger, Log_Send_File, Log_Receive_File, Log_Error_File
from general_configurations import BASE_DIR
from logging.handlers import RotatingFileHandler
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

class Datalogs:

    def errorlog(self, filename, level=logging.INFO):
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(lineno)d - %(levelname)s - %(message)s"
        )
        a = os.path.join(BASE_DIR, 'Logs', filename)
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