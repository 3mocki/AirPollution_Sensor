import sqlite3
from CalAQI import *

class MySqlite:

    # setting for db name
    def __init__(self, name):
        self.dbName = name + '.db'
        self.AirDataTableName = name + 'Air'

    # setting for db connection
    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def deleteTable(self):
        self.cursor.execute(' DROP TABLE IF EXISTS ' + self.AirDataTableName)

    def createTable(self):
        self.cursor.execute(' CREATE TABLE IF NOT EXISTS ' + self.AirDataTableName +
                            ' (num INTEGER PRIMARY KEY, temp FLOAT, no2 FLOAT, o3 FLOAT, co FLOAT, so2 FLOAT, pm25 FLOAT, pm10 FLOAT, no2aqi INT, o3aqi INT, co_aqi INT, so2aqi INT, pm25aqi INT, pm10aqi INT)')

    def insertData(self, temp, no2, o3, co, so2, pm25, pm10):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (temp, no2, o3, co, so2, pm25, pm10, no2aqi, o3aqi, co_aqi, so2aqi, pm25aqi, pm10aqi) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (temp, no2, o3, co, so2, pm25, pm10, 0, 0, 0, 0, 0, 0))

        # based on a hour (DEFAULT)
        if self.countData() > 10:
            self.cursor.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
        airAvg = self.getAvgData()
        calResNo2 = 0
        calResO3 = 0
        calResCo = 0
        calResSo2 = 0
        calResPm25 = 0
        calResPm10 = 0
        for x in range(0,6):
            if x == 0:
                calResNo2 = int(CalNo2Aqi(airAvg[0]))
            elif x == 1:
                calResO3 = int(CalO3Aqi_1(airAvg[1]))
            elif x == 2:
                calResCo = int(CalCoAqi(airAvg[2]))
            elif x == 3:
                calResSo2 = int(CalSo2Aqi(airAvg[3]))
            elif x == 4:
                calResPm25 = int(CalPm25Aqi(airAvg[4]))
            elif x == 5:
                calResPm10 = int(CalPm10Aqi(airAvg[5]))

    # calResData is sent to Communication Script
        self.cursor.execute(' UPDATE ' + self.AirDataTableName +
            ' set no2aqi =' + str(calResNo2) + ',o3aqi = ' + str(calResO3) + ',co_aqi = ' + str(calResCo) + ',so2aqi = ' + str(calResSo2) + ',pm25aqi = ' + str(calResPm25) + ',pm10aqi = ' + str(calResPm10) + ' where num = (SELECT MAX(num)  FROM ' + self.AirDataTableName +');')

    def countData(self):
    # SELECT COUNT(*) FROM TABLE NAME => Check How many data on the table
        self.cursor.execute(' SELECT COUNT(*) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return int(row[0])

    def getAvgData(self):
        self.cursor.execute(' SELECT avg(no2), avg(o3), avg(co), avg(so2), avg(pm25), avg(pm10) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return row

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()

    # def makeCSVformat(self, alldata):
    #     if alldata == True:
    #         airDataCSV = ''
    #         self.cursor.execute(' SELECT * from ' + self.allAirDataTableName + ' WHERE NUM = (SELECT MAX(NUM)  FROM ' + self.allAirDataTableName +');')
    #         for row in self.cursor:
    #             for x in range(1, 12):
    #                 airDataCSV += str(row[x]) + ','
    #         return airDataCSV