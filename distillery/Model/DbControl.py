import sqlite3
import os
import uuid
from datetime import date

class DBCntl():

    def __init__(self):

        self.db_path = './database/record.db'
        for root, dirs, files in os.walk('./database'):
            if 'record.db' not in files:
                self.createDB()

    def createDB(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''CREATE TABLE masterData
                            ([id] integer PRIMARY KEY autoincrement,[freshInstall] integer ,[startDate] text , [listOfDate] text)''')

        insert = 'INSERT INTO masterData (freshInstall, startDate, listOfDate) VALUES (?, ?, ?)'
        c.execute(insert, (1,'','',))

        c.execute('''CREATE TABLE distillery
                     ([id] integer PRIMARY KEY autoincrement  ,[distilleryName] text not null , [barrelTypeID] text not null )''')

        c.execute('''CREATE TABLE barrelCode
                     ([id] integer PRIMARY KEY autoincrement ,[barrelTypeCode] text, [barrelTypeID] text )''')

        c.execute('''CREATE TABLE BarrelAverage
                     ([id] integer PRIMARY KEY autoincrement ,[barrelTypeCodeID] text, [averageData] double, [exportDate] text not null , [distilleryID] text )''')

        conn.commit()
        conn.close()

    def checkIfFreshInstall(self, current_date):
        self.open()
        query = 'SELECT * FROM masterData '
        cursor = self.connection.execute(query).fetchone()
        if int(cursor[1]) == 1:
            update = "UPDATE masterData set freshInstall =  ? , startDate = ? , listOfDate = ?"

            self.connection.execute(update, (0,current_date, current_date, ))
            self.commit()
        else:
            listofDate = str(cursor[3])
            r = listofDate.split(',')
            if current_date not in r:
                listofDate  = listofDate + ','+current_date
                update = "UPDATE masterData set listOfDate = ? "
                self.connection.execute(update, (listofDate,))
                self.commit()
        self.close()

    def open(self):
        self.connection = sqlite3.connect(self.db_path)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def search(self, distilleryName, barrel , current_date):
        query = 'SELECT * FROM distillery where distilleryName =  ? '
        distillery_result = self.connection.execute(query ,(distilleryName,)).fetchall()
        if len(distillery_result) > 0:
            for row in distillery_result:
                    query = 'SELECT * FROM barrelCode where barrelTypeCode =  ? and  barrelTypeID = ? '
                    barrel_result = self.connection.execute(query, (barrel.key, str(row[2]),) ).fetchall()
                    if len(barrel_result) > 0:
                            query = 'SELECT * FROM BarrelAverage where barrelTypeCodeID = ?  and  exportDate = ?  and distilleryID  = ? '
                            average_result= self.connection.execute( query, (barrel.key, current_date,  distilleryName, )).fetchall()
                            if len(average_result) > 0:
                                update = "UPDATE BarrelAverage set averageData =  ?  where exportDate = ? and  barrelTypeCodeID =  ?  and distilleryID = ? "
                                self.connection.execute(update,(barrel.average,current_date, barrel.key, distilleryName,))
                            else:
                                insert = "INSERT INTO BarrelAverage (barrelTypeCodeID,averageData , exportDate, distilleryID ) VALUES (? , ? , ? , ? )"
                                self.connection.execute(insert ,(barrel.key, barrel.average, current_date, distilleryName, ))
                    else:
                        guid = str(row[2])
                        self.connection.execute("INSERT INTO barrelCode (barrelTypeCode, barrelTypeID) VALUES (?, ? )",(barrel.key, str(guid),) )
                        insert = "INSERT INTO BarrelAverage (barrelTypeCodeID,averageData , exportDate, distilleryID ) VALUES (? , ? , ? , ? )"
                        self.connection.execute(insert, (barrel.key, barrel.average, current_date, distilleryName,))
        else:
            self.createNewDistillery(distilleryName, barrel , current_date)

    def createNewDistillery(self, name, barrel ,current_date):
        guid = uuid.uuid1()
        insert = "INSERT INTO distillery (distilleryName,barrelTypeID) VALUES (?, ? )"
        self.connection.execute(insert, (name,str(guid),))
        insert = "INSERT INTO barrelCode (barrelTypeCode,barrelTypeID) VALUES (?, ? )"
        self.connection.execute(insert, (barrel.key, str(guid),))
        insert = "INSERT INTO BarrelAverage (barrelTypeCodeID,averageData , exportDate, distilleryID ) VALUES (? , ? , ? , ? )"
        self.connection.execute(insert, (barrel.key, barrel.average, current_date, name,))

    def getAllDistillery(self):

        query = "SELECT * FROM distillery"
        return self.connection.execute(query).fetchall()

    def getAllBarrelByID(self ,key ):
        query = "SELECT * FROM  barrelCode where  barrelTypeID = ? "
        return self.connection.execute(query, (key,)).fetchall()

    def getAllAverage(self , barrelCode_id, distillery_id ):
        query = "SELECT * FROM  BarrelAverage where  barrelTypeCodeID = ? and distilleryID = ?"
        return self.connection.execute(query, (barrelCode_id,distillery_id, )).fetchall()

    def getMasterData(self):
        return self.connection.execute('SELECT * FROM masterData ').fetchone()

    def clearTables(self):
        self.open()
        self.connection.execute('DELETE from distillery ')
        self.connection.execute('DELETE from barrelCode ')
        self.connection.execute('DELETE from BarrelAverage ')
        update = 'UPDATE masterData set freshInstall =  ? , startDate = ? ,  listOfDate = ?  '
        self.connection.execute(update, (1,'','',))
        self.commit()
        self.close()

