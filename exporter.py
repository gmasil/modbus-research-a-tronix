from pyModbusTCP.client import ModbusClient
import prometheus_client as prom
import numpy as np
import time

c = ModbusClient('192.168.178.36', port=502, unit_id = 247, timeout = 2, auto_open=True, auto_close=True)

registers = []
with open("legal-adresses.txt") as file:
    for line in file:
        line_data = line.rstrip().split()
        if len(line_data) == 1 or line_data[1] != "unused":
            registers.append(int(line_data[0]))


gauge = prom.Gauge('holding_register', 'Generic register gauge', ['register'])

register_gauges = []
for reg in registers:
    gauge.labels(register=reg).set(0)

prom.start_http_server(8998)

while True:
    for reg in registers:
        values = c.read_holding_registers(reg, 1)
        if values != None:
            value = int(np.uint16(values[0]).astype(np.int16))
            gauge.labels(register=reg).set(value)
