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


# class DataLogs(object):
#     """
#     Setup log files for data sending and data receiving.Log the data send to Azure. Log the data received from Azure.
#     Log the error while executing the code.
#     """
#     @classmethod
#     def setup_logger(cls, name, log_file, level=logging.INFO):
#         handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=2)
#         handler.setFormatter(formatter)
#         logger = logging.getLogger(name)
#         logger.setLevel(level)
#         logger.addHandler(handler)
#         return logger

#     # def send_data_logs(self, data):
#     #     logger = self.setup_logger(Sending_Logger, Log_Send_File)
#     #     logger.info(data)

#     # def receive_data_logs(self, data):
#     #     super_logger = self.setup_logger(Receiving_Logger, Log_Receive_File)
#     #     super_logger.info(data)

#     def error_log(self, data,sensor):
#         error_log = self.setup_logger(Error_Logger, f"{sensor}.log")
#         error_log.info(data)

class Datalogs:

    def errorlog(self, filename, level=logging.INFO):
        logger = logging.getLogger()
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(lineno)d - %(filename)s - %(levelname)s - %(message)s"
        )
        file_handler = RotatingFileHandler(
            os.path.join(BASE_DIR, "Logs", filename),
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