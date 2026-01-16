import logging
# from pymodbus.client import ModbusTcpClient
from pyModbusTCP.client import ModbusClient
import prometheus_client as prom
import numpy as np

# client = ModbusTcpClient('192.168.178.36', port=502)
# client.unit_id = 247
# client.connect()

#print(client.__dict__)

#client.read_coils(0)
#value = client.read_holding_registers(10994)
#value = client.read_input_registers(10994)
#print(value)

# logging.basicConfig()
# logging.getLogger('pyModbusTCP.client').setLevel(logging.DEBUG)

c = ModbusClient('192.168.178.36', port=502, unit_id = 247, timeout = 2, auto_open=True, auto_close=True)


values = c.read_holding_registers(31026, 1)
if values == None:
    print("None :(")
else:
    value = int(np.uint16(values[0]).astype(np.int16))
    print(value)
exit()

# print(c.read_device_identification())
# print(c.read_coils(4300, 16))

# register 43000 is SOC
registers = []
with open("legal-adresses.txt") as file:
    for line in file:
        line_data = line.rstrip().split()
        if len(line_data) == 1 or line_data[1] != "unused":
            registers.append(int(line_data[0]))

for reg in registers:
    print(str(reg))

exit()

# find SOC
# registers = []
# registers.append(31038)
# registers.append(32038)



# for reg in range(0, 65535):
while len(registers) > 0:
    values = {}
    tmp_registers = registers
    for reg in registers:
        value = c.read_holding_registers(reg, 1)
        if value == None:
            print("trying address " + str(reg) + ": " + c.last_except_as_txt)
            tmp_registers.remove(reg)
        else:
            if len(registers) > 30:
                print("" + str(reg) + ": " + str(value[0]))
            values[reg] = value[0]
            # if value[0] < 8 or value[0] > 12:
            #     tmp_registers.remove(reg)
    registers = tmp_registers
    for reg in range(0, 10):
        print("")
    print("start, regs: " + str(len(registers)))
    print("")
    for reg in registers:
        print(reg)
    print("")
    if(len(registers) <= 30):
        for reg, value in values.items():
            print(str(reg) + " : " + str(value))
