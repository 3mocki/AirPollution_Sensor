# 1 hour
def CalNo2Aqi(no2aver):
    if 0 <= no2aver <= 53:
        no2aqi = (((no2aver - 0) * (50 - 0)) / (53 - 0)) + 0
        return no2aqi
    elif 54 <= no2aver <= 100:
        no2aqi = (((no2aver - 54) * (100 - 51)) / (100 - 54)) + 51
        return no2aqi
    elif 101 <= no2aver <= 360:
        no2aqi = (((no2aver - 101) * (150 - 101)) / (360 - 101)) + 101
        return no2aqi
    elif 361 <= no2aver <= 649:
        no2aqi = (((no2aver - 361) * (200 - 151)) / (649 - 361)) + 151
        return no2aqi
    elif 650 <= no2aver <= 1249:
        no2aqi = (((no2aver - 650) * (300 - 201)) / (1249 - 650)) + 201
        return no2aqi
    elif 1250 <= no2aver <= 2049:
        no2aqi = (((no2aver - 1250) * (500 - 301)) / (1649 - 1250)) + 301
        return no2aqi
    else:
        return 501

# 1 hour
def CalO3Aqi_1(o3aver_1):
    if 0 <= o3aver_1 <= 0.059:
        o3aqi = (((o3aver_1 - 0) * (50 - 0)) / (0.059 - 0)) + 0
        return o3aqi
    elif 0.060 <= o3aver_1 <= 0.075:
        o3aqi = (((o3aver_1 - 0.060) * (100 - 51)) / (0.075 - 0.060)) + 51
        return o3aqi
    elif 0.076 <= o3aver_1 <= 0.095:
        o3aqi = (((o3aver_1 - 0.076) * (150 - 101)) / (0.095 - 0.076)) + 101
        return o3aqi
    elif 0.096 <= o3aver_1 <= 0.115:
        o3aqi = (((o3aver_1 - 0.096) * (200 - 151)) / (0.115 - 0.096)) + 151
        return o3aqi
    elif 0.116 <= o3aver_1 <= 0.374:
        o3aqi = (((o3aver_1 - 0.116) * (300 - 201)) / (0.374 - 0.116)) + 201
        return o3aqi
    else:
        return 501

# 8 hour
def CalO3Aqi_8(o3aver_8):
    if 0.125 <= o3aver_8 <= 0.164:
        o3aqi = (((o3aver_8-0.125) * (150-101)) / (0.164-0.125)) + 101
        return o3aqi
    elif 0.165 <= o3aver_8 <= 0.204:
        o3aqi = (((o3aver_8-0.165) * (200-151)) / (0.204-0.165)) + 151
        return o3aqi
    elif 0.205 <= o3aver_8 <= 0.404:
        o3aqi = (((o3aver_8-0.205) * (300-201)) / (404-205)) + 201
        return o3aqi
    elif 0.405 <= o3aver_8 <= 0.604:
        o3aqi = (((o3aver_8-0.405) * (300-201)) / (504-405)) + 301
        return o3aqi
    else:
        return 501

# 8 hour
def CalCoAqi(coaver):
    if 0 <= coaver <= 4.4:
        co_aqi = (((coaver - 0) * (50 - 0)) / (4.4 - 0)) + 0
        return co_aqi
    elif 4.5 <= coaver <= 9.4:
        co_aqi = (((coaver - 4.5) * (100 - 51)) / (9.4 - 4.5)) + 51
        return co_aqi
    elif 9.5 <= coaver <= 12.4:
        co_aqi = (((coaver - 9.5) * (150 - 101)) / (12.4 - 9.5)) + 101
        return co_aqi
    elif 12.5 <= coaver <= 15.4:
        co_aqi = (((coaver - 12.5) * (200 - 151)) / (15.4 - 12.5)) + 151
        return co_aqi
    elif 15.5 <= coaver <= 30.4:
        co_aqi = (((coaver - 15.5) * (300 - 201)) / (30.4 - 15.5)) + 201
        return co_aqi
    elif 30.5 <= coaver <= 50.4:
        co_aqi = (((coaver - 30.5) * (500 - 301)) / (50.4 - 30.5)) + 301
        return co_aqi
    else:
        return 501

# 1 hour
def CalSo2Aqi(so2aver):
    if 0 <= so2aver <= 35:
        so2aqi = (((so2aver - 0) * (50 - 0)) / (35 - 0)) + 0
        return so2aqi
    elif 36 <= so2aver <= 75:
        so2aqi = (((so2aver - 36) * (100 - 51)) / (75 - 36)) + 51
        return so2aqi
    elif 76 <= so2aver <= 185:
        so2aqi = (((so2aver - 76) * (150 - 101)) / (185 - 76)) + 101
        return so2aqi
    elif 186 <= so2aver <= 304:
        so2aqi = (((so2aver - 186) * (200 - 151)) / (304 - 186)) + 151
        return so2aqi
    elif 305 <= so2aver <= 604:
        so2aqi = (((so2aver - 305) * (300 - 201)) / (604 - 305)) + 201
        return so2aqi
    elif 605 <= so2aver <= 1004:
        so2aqi = (((so2aver - 605) * (500 - 301)) / (1004 - 605)) + 301
        return so2aqi
    else:
        return 501

# 24 hour
def CalPm25Aqi(pm25aver):
    if 0 <= pm25aver <= 15.4:
        pm25aqi = (((pm25aver - 0) * (50 - 0)) / (15.4 - 0)) + 0
        return pm25aqi
    elif 15.5 <= pm25aver <= 40.4:
        pm25aqi = (((pm25aver - 15.5) * (100 - 51)) / (40.4 - 15.5)) + 51
        return pm25aqi
    elif 40.4 <= pm25aver <= 65.4:
        pm25aqi = (((pm25aver - 40.4) * (150 - 101)) / (65.4 - 40.4)) + 101
        return pm25aqi
    elif 65.5 <= pm25aver <= 150.4:
        pm25aqi = (((pm25aver - 65.5) * (200 - 151)) / (150.4 - 65.5)) + 151
        return pm25aqi
    elif 150.5 <= pm25aver <= 250.4:
        pm25aqi = (((pm25aver - 150.5) * (300 - 201)) / (250.4 - 150.5)) + 201
        return pm25aqi
    elif 250.5 <= pm25aver <= 500.4:
        pm25aqi = (((pm25aver - 250.5) * (500 - 301)) / (500.4 - 250.5)) + 301
        return pm25aqi
    else:
        return 501

# 24 hour
def CalPm10Aqi(pm10aver):
    if 0 <= pm10aver <= 54:
        pm10aqi = (((pm10aver - 0) * (50 - 0)) / (54 - 0)) + 0
        return pm10aqi
    elif 55 <= pm10aver <= 154:
        pm10aqi = (((pm10aver - 55) * (100 - 51)) / (154 - 55)) + 51
        return pm10aqi
    elif 155 <= pm10aver <= 254:
        pm10aqi = (((pm10aver - 155) * (150 - 101)) / (254 - 155)) + 101
        return pm10aqi
    elif 255 <= pm10aver <= 354:
        pm10aqi = (((pm10aver - 255) * (200 - 151)) / (354 - 255)) + 151
        return pm10aqi
    elif 355 <= pm10aver <= 424:
        pm10aqi = (((pm10aver - 355) * (300 - 201)) / (424 - 355)) + 201
        return pm10aqi
    elif 425 <= pm10aver <= 604:
        pm10aqi = (((pm10aver - 425) * (500 - 301)) / (604 - 425)) + 301
        return pm10aqi
    else:
        return 501