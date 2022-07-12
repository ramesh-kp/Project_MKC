import logging
from General_Configurations import Log_Send_File, Log_Receive_File, Log_Error_File
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


class Data_Logs:
    def setup_logger(self, name, log_file, level=logging.INFO):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def send_data_logs(self, data):
        logger = self.setup_logger('Sending_Logger', Log_Send_File)
        logger.info(data)

    def receive_data_logs(self, data):
        super_logger = self.setup_logger('Receiving_Logger', Log_Receive_File)
        super_logger.info(data)

    def error_log(self, data):
        error_log = self.setup_logger('Error_Logger', Log_Error_File)
        error_log.info(data)
