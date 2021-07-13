# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 00:47:26 2021

@author: kolof
"""
class Logger:
    __filePath = 'D:\\Documents\\Учебная практика\\2020-2021\\Февраль 2021\\Код\log.log'
    logger = None
    
    #Создание логгера

    def __init__(self, logger_name):
        import logging
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        try:
            fh = logging.FileHandler(self.__filePath)
        except FileNotFoundError:
            log_path = 'log.log'
            fh = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
   # @staticmethod
    def add(self, message):
        self.logger.info(str(message))
    
    #@staticmethod
    def add_error(self, message):
        self.logger.error(str(message))
    
    #@staticmethod
    def add_warning(self, message):
        self.logger.warning(str(message))
    
    #@staticmethod
    def add_critical(self, message):
        self.logger.critical(str(message))
    #@staticmethod
    def add_debug(self, message):
        self.logger.debug(str(message))
        
if __name__ == "__main__":
    pass