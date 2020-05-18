
import requests
import xmltodict
import json
import csv
from datetime import date
import os
from Model.Model import  *
from Model.DbControl import *
from tests.TestCase.Test import  *
from Controller.XMLReader import *
class XMLParse():

     def __init__(self):
         self.url = 'https://www.whiskyinvestdirect.com/view_market_xml.do'
         self.csv_path = './Output/Log.csv'
         self.db = DBCntl()
         self.xml_read = None

     def getData(self, url = None):
         ur  = None
         if not url:
             ur = self.url
         else:
             ur = url
         response = None
         try:
             response = requests.get(ur)
             #response = TestData()
             #response.getData('./tests/TestCase/test_case_07.txt')

         except Exception as e:
                print('Error in requesting to url : ' + str(ur))
                return
         try:
            if response:
                self.xml_read  = XMLReader()
                self.xml_read .parse(response.text)
         except Exception as e:
             print('Error during parsing of xml data. error : ' + str(e))
             return

         try:
             self.compute()
             self.updateDB()
             self.updateCSV()
         except Exception as e:
             print('Error during computation. error : ' + str(e))
             return

         print('Succesfully created CSV.....')

     def compute(self):

         if self.xml_read:
            for distillery in self.xml_read.listOfDistillery:
                for barrel in distillery.listBarrelType:
                    result = 0

                    #Ignore pitch with no pair
                    if len(barrel.listOfPitch) < 2:
                        continue

                    divisor = 0
                    for index in  range(len(barrel.listOfPitch)):
                        for pos  in  range(index + 1,len(barrel.listOfPitch) ):
                            old = None
                            young = None
                            if (barrel.listOfPitch)[index].integerAge < (barrel.listOfPitch)[pos].integerAge:
                                old = (barrel.listOfPitch)[index]
                                young =  (barrel.listOfPitch)[pos]
                            else:
                                young = (barrel.listOfPitch)[index]
                                old =  (barrel.listOfPitch)[pos]

                            if  old.highestSalePrice > 0 or young.lowestBuyPrice > 0:
                                diff_price = old.highestSalePrice - young.lowestBuyPrice
                                diff_time =  young.integerAge - old.integerAge
                                if diff_time != 0:
                                    result = result +  diff_price/diff_time
                                divisor = divisor + 1
                    if divisor  > 0:
                        barrel.average = result/divisor


     def updateDB(self):
         current = date.today()
         current_format = current.strftime('%m/%d/%y')
         self.db.checkIfFreshInstall(current_format)
         self.db.open()
         if self.xml_read:
            for distillery in self.xml_read.listOfDistillery:
                for barrel in distillery.listBarrelType:
                        self.db.search(distillery.key, barrel, current_format)

         self.db.commit()
         self.db.close()

     def getListOfDate(self, listOfDate):
         result = listOfDate.split(',')
         return result

     def updateCSV(self):
         writeData=  []
         for root, dirs, files in os.walk('./output'):
             if 'log.csv' not in files:
                 f = open('./output/log.csv' , 'a+')
                 f.close()
                 break
         self.db.open()
         master = self.db.getMasterData()
         result = self.getListOfDate(str(master[3]))
         writeData = []
         header = []
         header.append('Distillery')
         header.append('BarrelType')
         for   d in result:
             header.append(d)
         writeData.append(header)
         listOfRows = []

         distilleries =  self.db.getAllDistillery()
         if len(distilleries) > 0:
             for distillery in distilleries:
                 barrels =  self.db.getAllBarrelByID(str(distillery[2]))
                 if len(barrels) > 0:
                     for barrel in barrels:
                        row  = []
                        row.append(str(distillery[1]))
                        row.append(str(barrel[1]))
                        averages = self.db.getAllAverage(str(barrel[1]),str(distillery[1]) )
                        if len(averages) > 0:
                            noData = True
                            for index  in range(len(result)) :
                                data = ' '
                                for ave in averages:
                                    if result[index] ==  str(ave[3]):
                                        if float(ave[2]) != 0:
                                            data = str(ave[2])
                                            noData = False
                                        else:
                                            data = ' '
                                        break
                                row.append(data)
                            if not noData :
                             listOfRows.append(row)

         writeData.extend(listOfRows)
         with open(self.csv_path, 'w' ,newline='') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in writeData:
                employee_writer.writerow(line)

