import sqlite3

class MySqlite_RAD:

    # setting for db name
    def __init__(self, name):
        self.dbName = name + '.db'
        self.AirDataTableName = name + 'Communication'

    # setting for db connection
    def connectDB(self):
        self.db = sqlite3.connect(self.dbName)
        self.cursor = self.db.cursor()

    def deleteData(self):
        self.cursor.execute(' DELETE FROM ' + self.AirDataTableName + ' WHERE NUM IN(SELECT NUM FROM ' + self.AirDataTableName + ' LIMIT 10) ')

    def createTable(self):
        self.cursor.execute(' CREATE TABLE IF NOT EXISTS ' + self.AirDataTableName +
                            ' ( num INTEGER PRIMARY KEY, ts INT, temp FLOAT, no2 FLOAT, o3 FLOAT, co FLOAT, so2 FLOAT, pm25 FLOAT, pm10 FLOAT, no2aqi INT, o3aqi INT, co_aqi INT, so2aqi INT, pm25aqi INT, pm10aqi INT)')

    def insertData(self, timestamp, temp, no2, o3, co, so2, pm25, pm10, no2aqi, o3aqi, co_aqi, so2aqi, pm25aqi, pm10aqi):
        self.cursor.execute(' INSERT INTO ' + self.AirDataTableName +
                            ' (ts, temp, no2, o3, co, so2, pm25, pm10, no2aqi, o3aqi, co_aqi, so2aqi, pm25aqi, pm10aqi) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                            (timestamp, temp, no2, o3, co, so2, pm25, pm10, 0, 0, 0, 0, 0, 0))

    def getData(self):
        self.cursor.execute(' SELECT * FROM ' + self.AirDataTableName)
        self.data = self.cursor.fetchall()
        #print('Database.py getData() => ', data)

    def commitDB(self):
        self.db.commit()

    def closeDB(self):
        self.cursor.close()
        self.db.close()
