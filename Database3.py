import sqlite3
from CalAQI import *

#for 24 hours DB
class MySqlite_24:
    calResPm25 = 0
    calResPm10 = 0
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
                            ' ( num INTEGER PRIMARY KEY, pm25 FLOAT, pm10 FLOAT, pm25aqi INT, pm10aqi INT)')

    def insertData(self, pm25, pm10, r):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (pm25, pm10, pm25aqi, pm10aqi) values(?, ?, ?, ?);',
                            (pm25, pm10, 0, 0))
        temp_pm25 = pm25
        temp_pm10 = pm10

        if r == 1:
            self.airAvg = self.getAvgData()

            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set pm25aqi = ' + str(self.calResPm25) + ',pm10aqi = ' + str(self.calResPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

        elif 2 <= r <= 86400:
            self.newAirAvg[0] = (self.airAvg[0] + temp_pm25) / 2
            self.newAirAvg[1] = (self.airAvg[1] + temp_pm10) / 2

            self.calResPm25 = int(CalPm25Aqi(self.newAirAvg[0]))
            self.calResPm10 = int(CalPm10Aqi(self.newAirAvg[1]))

            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set pm25aqi = ' + str(self.calResPm25) + ',pm10aqi = ' + str(self.calResPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')


        # based on a day
        elif r > 86400:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.newAirAvg[0] = (self.airAvg[0] + temp_pm25) / 2
                    self.calResPm25 = int(CalPm25Aqi(self.newAirAvg[0]))
                elif x == 1:
                    self.newAirAvg[1] = (self.airAvg[1] + temp_pm10) / 2
                    self.calResPm10 = int(CalPm10Aqi(self.newAirAvg[1]))

            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName +
                                ' set pm25aqi = ' + str(self.calResPm25) + ',pm10aqi = ' + str(self.calResPm10) + ' WHERE NUM = (SELECT MAX(NUM) FROM ' + self.AirDataTableName + ');')

    def getData(self):
        self.cursor.execute(' SELECT * FROM ' + self.AirDataTableName)
        self.data = self.cursor.fetchall()
        #print('Database.py getData() => ', data)

    def getAvgData(self):
        self.cursor.execute(
            ' SELECT avg(pm25), avg(pm10) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return row

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()
