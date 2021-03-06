import serial
import time
from Database import *
from Database2 import *
from Database3 import *

# air list; ppm is O3 and CO // ppb is NO2, SO2
air_list = ['no2', 'o3', 'co', 'so2', 'pm25', 'pm10']

# timestamp, temp, no2, o3, co, so2, pm25, pm10, i
data = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# calibration data of 25-000160 Indoor Sensor
we_zero = [295, 391, 347, 345]
ae_zero = [282, 390, 296, 255]
sens = [0.228, 0.399, 0.276, 0.318]

# temp_n is going to no2, o3, co, so2 in 2 X 2 list
temp_n = [[1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00, 2.70],
          [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 2.87],
          [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48, -0.80],
          [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 1.95]]

# path of gpio control files
port = '/dev/tty96B0'
ard = serial.Serial(port, 9600)
gpio_path = '/sys/class/gpio/'

path_dir_gpio36 = gpio_path + 'gpio36/direction'
path_dir_gpio13 = gpio_path + 'gpio13/direction'
path_dir_gpio12 = gpio_path + 'gpio12/direction'
path_dir_gpio69 = gpio_path + 'gpio69/direction'
path_dir = [path_dir_gpio36, path_dir_gpio13, path_dir_gpio12, path_dir_gpio69]

path_val_gpio36 = gpio_path + 'gpio36/value'
path_val_gpio13 = gpio_path + 'gpio13/value'
path_val_gpio12 = gpio_path + 'gpio12/value'
path_val_gpio69 = gpio_path + 'gpio69/value'
path_val = [path_val_gpio36, path_val_gpio13, path_val_gpio12, path_val_gpio69]


# set the gpio pins to OUTPUT mode
def init_direction():
    for i in range(4):
        with open(path_dir[i], 'w') as f:
            f.write("out")


# set the gpio pins the value to '0'
def init_gpio():
    for i in range(4):
        with open(path_val[i], 'w') as f:
            f.write('0')

# gpio controlling function
def gpio_control(num):
    init_gpio()
    if num % 2 == 1:
        with open(path_val[0], 'w') as f:
            f.write('1')
    if num % 4 > 1:
        with open(path_val[1], 'w') as f:
            f.write('1')
    if num % 8 > 3:
        with open(path_val[2], 'w') as f:
            f.write('1')
    if num % 16 > 7:
        with open(path_val[3], 'w') as f:
            f.write('1')

# get the voltage value
def adc_converter(value):
    adc = int(value)
    volt = float(adc * 5.0 / 1024)
    return volt

def temp_choice(tmp, x):
    if -30 <= tmp:
        return temp_n[x - 1][0]
    elif -30 <= tmp < -20:
        return temp_n[x - 1][1]
    elif -20 <= tmp < -10:
        return temp_n[x - 1][2]
    elif -10 <= tmp < 0:
        return temp_n[x - 1][3]
    elif 0 <= tmp < 10:
        return temp_n[x - 1][4]
    elif 10 <= tmp < 20:
        return temp_n[x - 1][5]
    elif 20 <= tmp < 30:
        return temp_n[x - 1][6]
    elif 30 <= tmp < 40:
        return temp_n[x - 1][7]
    elif 40 <= tmp <= 50:
        return temp_n[x - 1][8]

if __name__ == '__main__':
    print("=========Operating Sensor=========")
    db = MySqlite_1('hour1')
    db2 = MySqlite_8('hour8')
    db3 = MySqlite_24('hour24')

    db.connectDB()
    db2.connectDB()
    db3.connectDB()

    db.createTable()
    db2.createTable()
    db3.createTable()

    i=0

    try:
        while True:
            data[8] = i
            print('first:'+str(data[8]))
            # collecting air data
            for x in range(0, 6):
                init_direction()
                init_gpio()
                print('*******************************')
                data[0] = int(time.time())
                if x == 0:
                    # measuring temperature
                    gpio_control(x)
                    ardOut = ard.readline()
                    temp_low = ardOut.rstrip('\n')
                    temp_value = adc_converter(temp_low)
                    temp_result = (float(temp_value) - 0.5) * 100.0
                    if temp_result <= -30:
                        temp_result = -30
                    elif temp_result > 50:
                        temp_result = 50
                    print('Temperature : ' + str(round(temp_result, 2)) + 'degree celcius')
                    # choice temperature each sensor
                    data[1] = round(temp_result, 2)

                elif 1 <= x <= 4:
                    # Measuring Working Electrode
                    gpio_control(x * 2 - 1)
                    ardOut = ard.readline()
                    we_low = ardOut.rstrip('\n')
                    we_value = adc_converter(we_low)
                    print(air_list[x - 1] + ' WE : ' + str(round(we_value, 2)) + 'mV')

                    # Measuring Auxiliary Electrode
                    gpio_control(x * 2)
                    ardOut = ard.readline()
                    ae_low = ardOut.rstrip('\n')
                    ae_value = adc_converter(ae_low)
                    print(air_list[x - 1] + ' AE : ' + str(round(ae_value, 2)) + 'mV')

                    if x == 1:
                        temp = temp_choice(temp_result, x)
                        # calculating ppb & ppm
                        ppb_value = ((we_value * 1000 - we_zero[x - 1]) - temp * (ae_value * 1000 - ae_zero[x - 1])) / \
                                    sens[x - 1]
                        no2 = round(ppb_value, 2)
                        data[2] = no2
                        print(air_list[x - 1] + ' : ' + str(round(ppb_value, 2)) + 'ppb')

                    elif x == 2:
                        temp = temp_choice(temp_result, x)
                        # calculating ppb & ppm
                        ppb_value = ((we_value * 1000 - we_zero[x - 1]) - temp * (ae_value * 1000 - ae_zero[x - 1])) / \
                                    sens[x - 1]
                        o3 = round(ppb_value / 1000, 2)
                        data[3] = o3
                        print(air_list[x - 1] + ' : ' + str(round(ppb_value / 1000, 2)) + 'ppm')

                    elif x == 3:
                        temp = temp_choice(temp_result, x)
                        # calculating ppb & ppm
                        ppb_value = ((we_value * 1000 - we_zero[x - 1]) - temp * (ae_value * 1000 - ae_zero[x - 1])) / \
                                    sens[x - 1]
                        co = round(ppb_value / 1000, 2)
                        data[4] = co
                        print(air_list[x - 1] + ' : ' + str(round(ppb_value / 1000, 2)) + 'ppm')

                    elif x == 4:
                        temp = temp_choice(temp_result, x)
                        # calculating ppb & ppm
                        ppb_value = ((we_value * 1000 - we_zero[x - 1]) - temp * (ae_value * 1000 - ae_zero[x - 1])) / \
                                    sens[x - 1]
                        so2 = round(ppb_value, 2)
                        data[5] = so2
                        print(air_list[x - 1] + ' : ' + str(round(ppb_value, 2)) + 'ppb')

                    print('n Table :' + str(temp))

                elif x == 5:
                    gpio_control(x * 2 - 1)
                    ardOut = ard.readline()
                    pm25_low = ardOut.rstrip('\n')
                    pm25_value = adc_converter(pm25_low)
                    v = pm25_value
                    hppcf = 240 * (v ** 6) - 2491.3 * (v ** 5) + 9448.7 * (v ** 4) - 14840 * (v ** 3) + 10684 * (
                                v ** 2) + 2211.8 * v + 7.9623
                    ugm3 = .518 + .00274 * hppcf
                    pm25 = round(ugm3, 2)
                    data[6] = pm25
                    pm10 = round(ugm3, 2)
                    data[7] = pm10
                    print(air_list[x - 1] + ' : ' + str(round(ugm3, 2)) + 'ug/m^3')
                    print(air_list[x] + ' : ' + str(round(ugm3, 2)) + 'ug/m^3')
                    print('*******************************')

            db.insertData(data[0], data[1], data[2], data[3], data[5], data[8])  # timestamp, temp, no2, o3, so2
            db2.insertData(data[3], data[4], data[8])  # o3, co
            db3.insertData(data[6], data[7], data[8])  # pm10, pm25

            db.commitDB()
            db2.commitDB()
            db3.commitDB()

            i+=1
            print('second:'+str(data[8]))

    except KeyboardInterrupt:
        db.closeDB()
        db2.closeDB()
        db3.closeDB()
        print("Exit")

