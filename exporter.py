from pyModbusTCP.client import ModbusClient
import prometheus_client as prom
import numpy as np
import time
import json

verbose=False

# load sensors
sensors = json.loads(open('sensors.json').read())

# prepare sensors and gauges
for sensor in sensors:
    sensor["used"] = False
    if sensor.get("unique_id") is None:
        print("Found metric without unique_id")
        exit(1)
    if sensor.get("name") is None:
        print("Metric " + sensor.get("unique_id") + " does not have a name")
        exit(2)
    if sensor.get("address") is None:
        print("Metric " + sensor.get("unique_id") + " (" + sensor.get("name") + ") does not have an address")
        exit(3)
    if sensor.get("data_type") is None:
        if verbose:
            print("Ignoring metric " + sensor.get("unique_id") + " (" + sensor.get("name") + "): data_type is not specified")
        continue
    if sensor.get("data_type") != "uint16" and sensor.get("data_type") != "int16":
        if verbose:
            print("Ignoring metric " + sensor.get("unique_id") + " (" + sensor.get("name") + "): data_type " + sensor.get("data_type") + " is not recognized")
        continue
    if sensor.get("unit_of_measurement") is None:
        if verbose:
            print("Ignoring metric " + sensor.get("unique_id") + " (" + sensor.get("name") + "): unit_of_measurement is not specified")
        continue
    if sensor.get("input_type") is None:
        if verbose:
            print("Ignoring metric " + sensor.get("unique_id") + " (" + sensor.get("name") + "): input_type is not specified")
        continue
    if sensor.get("input_type") != "holding":
        if verbose:
            print("Ignoring metric " + sensor.get("unique_id") + " (" + sensor.get("name") + "): input_type " + sensor.get("input_type") + " is not recognized")
        continue
    if sensor.get("scale") is None:
        sensor["scale"] = 1.0
    elif isinstance(sensor.get("scale"), int):
        sensor["scale"] = float(sensor.get("scale"))
    elif isinstance(sensor.get("scale"), float) == False:
        print("Metric " + sensor.get("unique_id") + " (" + sensor.get("name") + ") has an invalid scale: " + str(sensor.get("scale")))
        exit(3)
    sensor["gauge"] = prom.Gauge(sensor.get("unique_id"), sensor.get("name"), ['address', 'data_type', 'scale', 'unit_of_measurement'])
    sensor["used"] = True

def update_sensor(client, sensor):
    if sensor["used"]:
        values = client.read_holding_registers(sensor.get("address"), 1)
        if values != None:
            if sensor.get("data_type") == "uint16":
                value = values[0]
            else:
                value = int(np.uint16(values[0]).astype(np.int16))
            sensor["gauge"].labels(address = sensor.get("address"), data_type = sensor.get("data_type"), scale = sensor.get("scale"), unit_of_measurement = sensor.get("unit_of_measurement")).set(value)

# connect to modbus client
c = ModbusClient('192.168.178.36', port=502, unit_id = 247, timeout = 2, auto_open=True, auto_close=True)

# start server
prom.start_http_server(8998)

# update values
while True:
    for sensor in sensors:
        update_sensor(c, sensor)
