import os
import serial   # pip install pyserial
import pynmea2  # pip install pynmea2 - https://github.com/Knio/pynmea2


def startGPS():
    os.system('sudo systemctl start qdsp-start.service')
    os.system('sudo systemctl start gnss-gpsd.service')
    os.system('sudo systemctl start qmi-gps-proxy.service')
    os.system('sudo systemctl restart gpsd')


def main():
    # Starts all services to enable GPS
    startGPS()

    # Open the GPS serial port
    gps = serial.Serial('/dev/ttyGPS0')

    while True:
        # Read and parse GPS data
        data = gps.readline()
        i = data.find('$GPGGA')
        if (i > 0):
            msg = pynmea2.parse(data[i:])
            print 'Latitude: ' + str(msg.latitude) + ' | Longitude: ' + str(msg.longitude)


if __name__ == '__main__':
    try:
        main()
    except FatalError as e:
        print '\nA fatal error occurred: %s' % e
        gps.close()
        sys.exit(2)
    except KeyboardInterrupt:
        print '\nExit'
        gps.close()