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
        self.cursor.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 10) ')

    def createTable(self):
        self.cursor.execute(' CREATE TABLE IF NOT EXISTS ' + self.AirDataTableName +
                            ' ( num INTEGER PRIMARY KEY, ts INT, temp FLOAT, no2 FLOAT, o3 FLOAT, co FLOAT, so2 FLOAT, pm25 FLOAT, pm10 FLOAT, no2aqi INT, o3aqi INT, co_aqi INT, so2aqi INT, pm25aqi INT, pm10aqi INT)')

    def insertData(self, timestamp, temp, no2, o3, co, so2, pm25, pm10):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (ts, temp, no2, o3, co, so2, pm25, pm10, no2aqi, o3aqi, co_aqi, so2aqi, pm25aqi, pm10aqi) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                            (timestamp, temp, no2, o3, co, so2, pm25, pm10, 0, 0, 0, 0, 0, 0))
        calResNo2 = ""
        calResO3 = ""
        calResCo = ""
        calResSo2 = ""
        calResPm25 = ""
        calResPm10 = ""
        # based on a hour (DEFAULT)
        # if self.countData() > 3600:
        #     self.cursor.execute(
        #         ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
        airAvg = self.getAvgData()
        for x in range(0, 6):
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
                            ' set no2aqi =' + str(calResNo2) + ',o3aqi = ' + str(calResO3) + ',co_aqi = ' + str(
            calResCo) + ',so2aqi = ' + str(calResSo2) + ',pm25aqi = ' + str(calResPm25) + ',pm10aqi = ' + str(
            calResPm10) + ' where num = (SELECT MAX(num)  FROM ' + self.AirDataTableName + ');')

    def deleteData(self):
        self.curser.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE ')


    def getData(self):
        self.cursor.execute(' SELECT * FROM ' + self.AirDataTableName)
        self.data = self.cursor.fetchall()
        #print('Database.py getData() => ', data)

    def countData(self):
        # SELECT COUNT(*) FROM TABLE NAME => Check How many data on the table
        self.cursor.execute(' SELECT COUNT(*) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return int(row[0])

    def getAvgData(self):
        self.cursor.execute(
            ' SELECT avg(no2), avg(o3), avg(co), avg(so2), avg(pm25), avg(pm10) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return row

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.commit()
        self.db.close()