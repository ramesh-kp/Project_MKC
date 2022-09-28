import logging
from General_Configurations import Log_Send_File, Log_Receive_File, Log_error_File
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

class Data_Logs:         
    def Setup_Logger(self, name, log_file, level=logging.INFO):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def Send_Data_Logs(self, data):
        logger = self.Setup_Logger('Sending_Logger', Log_Send_File)
        logger.info(data)

    def Receive_Data_Logs(self, data):
        super_logger = self.Setup_Logger('Receiving_Logger', Log_Receive_File)
        super_logger.info(data)
    def Error_log(self,data):
        error_log = self.Setup_Logger('Error_Logger', Log_error_File)
        error_log.info(data)
