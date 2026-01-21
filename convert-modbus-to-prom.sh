#! /bin/bash

cat configuration-modbus.yaml | yq '.modbus[].sensors' -o=json | jq '[.[] | .expr = (.unique_id|tostring) + " * " + (.scale|tostring) | del(.scan_interval, .slave, .address, .data_type, .scale, .precision, .input_type)]' | jq '[.[] | {name,unique_id,expr,unit_of_measurement,device_class,state_class}]' | jq 'del(..|nulls)' | yq -P | sed 's/ \* 1$//g' | sed 's/ \* null$//g' | yq '.'
