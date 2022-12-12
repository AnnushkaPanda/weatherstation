
#!/usr/bin/env python

# Python Modules
import serial
import json
import sys
import time
import influxdb_client
from time import gmtime, strftime
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "<your-token>"
url = "http://influxdbV2:8086"
org = "m<-org"
bucket = "weather"
measurement = "Messungen"
location = "my-location"

# Configuration
serialPort = '/dev/ttyUSB0'

# Open serial port
try:
    ser = serial.Serial(serialPort, baudrate=9600, timeout=None)
except:
    sys.exit(1)
# Main loop
while True:
    # Wait for data and try error recovery on disconnect
    try:
        now = datetime.now()
        timestamp_aq = datetime.timestamp(now)
        iso = datetime.utcnow()
        serData = ser.readline()
        dataset = str(serData).split(';')
        # Parse meter readings into dictionary (abbr. to rd for typing laziness of yours truely)
        rd = {}
        n = 1
        for n in range(1, 9):
            # Conversion from german decimal mark , to international .
            try:
                rd['temp'+str(n)] = float(dataset[2+n].replace(',', '.'))
            except ValueError:
                pass
            try:
                rd['hum'+str(n)] = float(dataset[10+n].replace(',', '.'))
            except ValueError:
                pass
        # Kombisensor is mapped to temp9/hum9
        try:
            rd['temp9'] = float(dataset[19].replace(',', '.'))
        except ValueError:
            pass
        try:
            rd['hum9'] = float(dataset[20].replace(',', '.'))
        except ValueError:
            pass
        try:
            rd['windspeed'] = float(dataset[21].replace(',', '.'))
        except ValueError:
            pass
        try:
            rd['rainfall'] = float(dataset[22].replace(',', '.'))
        except ValueError:
            pass
        # Write Dictionary to InfluxDB
        try:
            with InfluxDBClient(url=url, token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                loaded = [
                    {
                        "measurement": measurement,
                        "tags": {
                            "Ort": location,
                            "domain": "sensor"
                        },
                        "time": iso,
                        "fields": rd
                    }
                ]
                print(loaded)
                write_api.write(bucket=bucket, record=loaded)
            time.sleep(120)
        except KeyboardInterrupt:
            write_api.__del__()
            client.__del__()
            ser.close()
            ser = serial.Serial(serialPort, baudrate=9600, timeout=None)
            sys.exit()
            pass
    except serial.SerialException as e:
        try:
            ser.close()
            ser = serial.Serial(serialPort, baudrate=9600, timeout=None)
            sys.exit()
        except:
            pass