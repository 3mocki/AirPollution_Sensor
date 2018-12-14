import sqlite3
from CalAQI import *

# for 8 hours DB
class MySqlite_8:
    calResO3=0
    calResCo=0
    airAvg = [0, 0]
    newAirAvg = [0, 0]

    # setting for db name
    def __init__(self, name):
        self.dbName = name + '.db'
        self.AirDataTableName = name + 'Air'

    # setting for db connection
    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def createTable(self):
        self.cursor.execute(' CREATE TABLE IF NOT EXISTS ' + self.AirDataTableName +
                            ' ( num INTEGER PRIMARY KEY, o3 FLOAT, co FLOAT, o3aqi INT, co_aqi INT)')

    def insertData(self, o3, co, z):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (o3, co, o3aqi, co_aqi) values(?, ?, ?, ?);',
                            (o3, co, 0, 0))
        temp_o3 = o3
        temp_co = co

        if z == 1:
            self.airAvg = self.getAvgData()
            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                ' set co_aqi = ' + str(self.calResCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

        elif 2 <= z <= 28800:
            self.newAirAvg[1] = (self.airAvg[1] + temp_co) / 2
            self.calResCo = int(CalCoAqi(self.newAirAvg[1]))
            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                ' set co_aqi = ' + str(self.calResCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

        # based on 8 hours
        elif z > 28800:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.newAirAvg[0] = (self.airAvg[0] + temp_o3) / 2
                    self.calResO3 = int(CalO3Aqi_8(self.newAirAvg[0]))
                elif x == 1:
                    self.newAirAvg[1] = (self.airAvg[1] + temp_co) / 2
                    self.calResCo = int(CalCoAqi(self.newAirAvg[1]))

            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                ' set o3aqi = ' + str(self.calResO3) + ',co_aqi = ' + str(self.calResCo) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

    def getData(self):
        self.cursor.execute(' SELECT * FROM ' + self.AirDataTableName)
        self.data = self.cursor.fetchall()
        #print('Database.py getData() => ', data)

    def getAvgData(self):
        self.cursor.execute(
            ' SELECT avg(o3), avg(co) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return row

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()