import sqlite3
from CalAQI import *

# for a hour DB
class MySqlite_1:
    calResNo2 = 0
    calResO3 = 0
    calResSo2 = 0
    airAvg = [0, 0, 0]
    newAirAvg=[0, 0, 0]

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
                            ' (num INTEGER PRIMARY KEY, ts INT, temp FLOAT, no2 FLOAT, o3 FLOAT, so2 FLOAT, no2aqi INT, o3aqi INT, so2aqi INT) ')

    def insertData(self, timestamp, temp, no2, o3, so2, i):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (ts, temp, no2, o3, so2, no2aqi, o3aqi, so2aqi) values(?, ?, ?, ?, ?, ?, ?, ?);',
                            (timestamp, temp, no2, o3, so2, 0, 0, 0))
        temp_no2 = no2
        temp_o3 = o3
        temp_so2 = so2

        if i == 1:
            self.airAvg = self.getAvgData()
            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calResNo2) + ',o3aqi =' + str(self.calResO3) + ',so2aqi =' + str(self.calResSo2) + ' WHERE NUM = (SELECT MAX(NUM)  FROM ' + self.AirDataTableName + ');')


        elif 2 <= i <= 3600:
            self.newAirAvg[0] = (self.airAvg[0] + temp_no2) / 2
            self.newAirAvg[1] = (self.airAvg[1] + temp_o3) / 2
            self.newAirAvg[2] = (self.airAvg[2] + temp_so2) / 2

            self.calResNo2 = int(CalNo2Aqi(self.newAirAvg[0]))
            self.calResO3 = int(CalO3Aqi_1(self.newAirAvg[1]))
            self.calResSo2 = int(CalSo2Aqi(self.newAirAvg[2]))

            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calResNo2) + ',o3aqi =' + str(self.calResO3) + ',so2aqi =' + str(self.calResSo2) + ' WHERE NUM = (SELECT MAX(NUM)  FROM ' + self.AirDataTableName + ');')


        # based on a hour (DEFAULT)
        elif 3600 < i < 28800:
            self.cursor.execute(
                ' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 2):
                if x == 0:
                    self.newAirAvg[0] = (self.airAvg[0] + temp_no2) / 2
                    self.calResNo2 = int(CalNo2Aqi(self.newAirAvg[0]))
                elif x == 1:
                    self.newAirAvg[1] = (self.airAvg[1] + temp_o3) / 2
                    self.calResO3 = int(CalO3Aqi_1(self.newAirAvg[1]))
                elif x == 2:
                    self.newAirAvg[2] = (self.airAvg[2] + temp_so2) / 2
                    self.calResSo2 = int(CalSo2Aqi(self.newAirAvg[2]))
            # calResData is sent to Communication Script
            self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calResNo2) + ',o3aqi = ' + str(self.calResO3) + ',so2aqi = ' + str(self.calResSo2) + ' WHERE NUM = (SELECT MAX(NUM)  FROM ' + self.AirDataTableName + ');')


        elif i > 28800:
            self.cursor.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 1) ')
            for x in range(0, 1):
                if x == 0:
                    self.newAirAvg[0] = (self.airAvg[0] + temp_no2) / 2
                    self.calResNo2 = int(CalNo2Aqi(self.newAirAvg[0]))
                elif x == 1:
                    self.newAirAvg[2] = (self.airAvg[2] + temp_so2) / 2
                    self.calResSo2 = int(CalSo2Aqi(self.newAirAvg[2]))

                # calResData is sent to Communication Script
                self.cursor.execute(' UPDATE ' + self.AirDataTableName + ' set no2aqi =' + str(self.calResNo2) + ',so2aqi = ' + str(self.calResSo2) + ' WHERE NUM = (SELECT MAX(NUM)  FROM ' + self.AirDataTableName + ');')

    def getData(self):
        self.cursor.execute(' SELECT * FROM ' + self.AirDataTableName)
        self.data = self.cursor.fetchall()
        # print('Database.py getData() => ', data)

    def getAvgData(self):
        self.cursor.execute(
            ' SELECT avg(no2), avg(o3), avg(so2) FROM ' + self.AirDataTableName)
        for row in self.cursor:
            return row

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()