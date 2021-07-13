# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:22:06 2021

@author: kolof
"""
import os
import pandas
import zipfile
from Logger import Logger

class DataPreparer:

    #создание класса 
    def __init__(self, zipFilesPath, xmlSavePath, log):

        self._zipFilesPath = zipFilesPath 
        self._xmlSavePath = xmlSavePath
        self.z = None
        self.log = log
    
    #смена директории хранения zip файлов
    def changeZipDirectory(self, newDirectory):
        self._zipFilesPath = newDirectory
        
    #смена директории хранения xml-файлов
    def changeXMLDirectory(self, newDirectory):
        self._xmlSavePath = newDirectory
    
    #чтение zip-файла
    def openZip(self, file):
        if os.path.exists(file):
            if zipfile.is_zipfile(file):
                self.z = zipfile.ZipFile(file, 'r')
                self.log.add('Открытие файла ' + os.path.basename(file) )
            else:
                raise FileNotFoundError
                self.log.add_error('Не удалось открыть файл ' + os.path.basename(file))
    
    #Извлечение всех файлов
    def extractZip(self, filetype = None):
        if self.z:
            self.log.add('Извлечение данных из файла ' + self.z.filename)
            if not filetype:
                self.z.extractall(self._xmlSavePath)
            else:
                for file in self.z.infolist():
                    if file.filename.endswith('.' + filetype):
                        self.z.extract(file.filename, self._xmlSavePath)
            self.z.close()
        else:
            raise FileNotFoundError
    
    #Открыть и извлечь файл
    def openAndExtractZip(self, file, filetype = None):
        self.openZip(file)
        self.extractZip(filetype)
        
    #Извлечение всех zip-файлов из активной директории
    def openAndExtractAllZip(self, filetype = None):
      with os.scandir(self._zipFilesPath) as listOfEntries:
          for entry in listOfEntries:
              print ('открываю файл', entry)
              self.openAndExtractZip(entry, filetype)      
    
    #Закрытие zip-файла
    def close(self):
        if self.z:
            self.z.close()
    
    #Имя файла
    @property
    def filename(self):
        return os.path.basename(self.z)
    
    #Путь активной xmlдиректории
    @property
    def xmlRoute(self):
        return self._xmlSavePath
    
    #Путь активной zip директории
    @property
    def zipRoute(self):
        return self._zipFilesPath
    
zipFilesPath = 'D:\\Documents\\Учебная практика\\2020-2021\\Февраль 2021\\Код\\Data\\Raw'
xmlSavePath = 'D:\\Documents\\Учебная практика\\2020-2021\\Февраль 2021\\Код\\Data\\Prepared\\extractedXml'
zipReader = DataPreparer(zipFilesPath, xmlSavePath, Logger('log'))
zipReader.openAndExtractAllZip(filetype = 'xml')
