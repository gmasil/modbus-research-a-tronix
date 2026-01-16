# Holding Registers for A-Trnox Inverter

# Certain Values
Battery SOC %: 31038
PV Power W: 31064
House Consumption W: 31127
Battery Charge Rate W: 31036
Grid W: 31066


find out grid:
`holding_register{register="31064"} + ignoring(register) holding_register{register="31036"} - ignoring(register) holding_register{register="31127"} or holding_register{register="31066"}`

all found normallized:
`( (holding_register{instance="localhost:8998",register=~"31038|31064|31127|31036|31066"} > 32000) - 65535 or (holding_register{instance="localhost:8998",register=~"31038|31064|31127|31036|31066"} <= 32000) )`

## SOC Battery
* 31038
* 32038

## PV Power
* 31064

also plausible (a little too high):
* 41022
* 39119

## Load of House
* 31127
* 31125 (maybe this is how much goes out from inverter (load house + into grid))

31127 tends to be slightly higher, seems a bit more plausible, but has slightly less movement

also similar, but seem to include difference to GRID? value too high under little load, too small under high load:
* 31056
* 39135

# Power into Battery
* 31036
negative value is chanrge
positive value is draw energy




# Archive

## Power drawn from Battery
* 31070
* 31027

these move similar, but are about 200W too high, never reach zero

* 31057
* 31058
* 31059
* 31012
* 31013
* 31014