# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:14:19 2021

@author: kolof
"""
from ftplib import FTP 
import ftplib
import os 
from Logger import Logger

class FTPLoader:

    #атрибуты подключения
    address = '' #ftp.zakupki.gov.ru
    login = '' #free
    password = '' #free
    _ftp = None
    _regionSelected = False
    _region = '' 
    
    #Создание объекта подключения. Указание данных для подключения
    def __init__(self, address, login, password, log):
        self.address = address
        self.login = login
        self.password = password
        self.log = log
        self.connect()
        
    #Подключение к серверу
    def connect(self):
        self._ftp = FTP(self.address)    
        if self._ftp.login(self.login, self.password):
            self.log.add('Подключение к ftp-серверу ' + str(self.address))
        else:
            raise ftplib.error_perm
            self.log.add_error('Ошибка подключения к ftp-серверу ' + str(self.address))
        
        
    #Проверка подключения к серверу
    def check(self):     
        if self._ftp.voidcmd('NOOP'):
            return True
        else:
            return False
        
    #Отключение от FTP-сервера
    def quit(self):
        self._ftp.quit()
        self.log.add('Выполнено отключение от ftp-сервера ' + str(self.address))
        
    #Переход в директорию региона
    def change_region(self, region):
        self._region = region
        self._ftp.cwd('fcs_regions/' + region)
        self._regionSelected = True
    
    #Переход в директорию currMonth региона
    def selectCurrMonth(self):
        if self._regionSelected:
            print('fcs_regions/' + self._region + '/notifications/currMonth')
            self._ftp.cwd('/fcs_regions/' + self._region + '/notifications/currMonth')
        
        else:
            print('Не выбран регион')
 
    #Переход в директорию prevMonth региона
    def selectPrevMonth(self):
        if self._regionSelected:
            self._ftp.cwd('/fcs_regions/' + self._region + '/notifications/prevMonth')
        else:
            print('Не выбран регион')
    
    #Загрузить все файлы из активной директории
    def loadAllFiles(self):
        filenames = self._ftp.nlst()
        for filename in filenames:
            self.loadFile(filename, out = False)
        #self.quit()
            
    #Загрузить файл по его имени
    def loadFile(self, filename, out = True):
        
        if self.check():
            filePath =  os.path.join('D:\\Documents\\Учебная практика\\2020-2021\Февраль 2021\\Код\\Data\\Raw',
                                    filename)       
            try:
                with open(filePath, 'wb') as localFile:
                    self.log.add('Загрузка файла ' + str(filename))
                    fileResponseMessage = self._ftp.retrbinary('RETR ' + filename, localFile.write, 8*1024)
                    self.log.add(fileResponseMessage)
            except ftplib.error_perm:   
                self.log.add_error('Ошибка при попытке выполнить загрузку файлов')
            if out:
                self.quit()
        
    @property
    #Список файлов и папок текущей директории
    def getList(self):
        return self._ftp.retrlines('LIST')
    
    @property
    def route(self):
        return self._ftp.pwd()
    
    


#Подключение к файлу госзакупок
connection = FTPLoader('ftp.zakupki.gov.ru', 'free', 'free', Logger('log')) 
connection.change_region('Komi_Resp')
connection.selectCurrMonth()
connection.loadAllFiles()

    
        