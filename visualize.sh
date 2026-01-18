#! /bin/bash



# echo "Battery Charge: ${data[0]}W"
# echo "SOC: ${data[1]}%"
# echo "PV Power: ${data[2]}W"
# echo "Grid: ${data[3]}W"
# echo "Consumption: ${data[4]}W"

clear
tput cup 0 0
echo '+-----------+                                        '
echo '|PV         |                                        '
echo '|           |                                        '
echo '|           |                                        '
echo '+-----+-----+                                        '
echo '      |                                              '
echo '      |                                              '
echo '      |                                              '
echo '      |                                              '
echo '      |                                              '
echo '+-----+-----+                           +-----------+'
echo '|Inverter   |                           |Load       |'
echo '|           +-----------------+---------+           |'
echo '|           |                 |         |           |'
echo '+-----+-----+                 |         +-----------+'
echo '      |                       |                      '
echo '      |                       |                      '
echo '      |                       |                      '
echo '      |                       |                      '
echo '      |                       |                      '
echo '+-----+-----+           +-----+-----+                '
echo '|Battery    |           |Grid       |                '
echo '|           |           |           |                '
echo '|           |           |           |                '
echo '+-----------+           +-----------+                '

animate_line() {
    y=$1
    x=$2
    length=$3
    direction=$4
    offset=$5

    if [ $direction == "down" ]; then
        dx=0
        dy=1
        line='|'
    elif [ $direction == "right" ]; then
        dx=1
        dy=0
        line='-'
    fi

    for i in $(seq 1 $length); do
        tput cup $y $x
        if [ $((($i + $offset) % 4)) == 0 ]; then
            echo '*'
        else
            echo "$line"
        fi
        let x=x+dx
        let y=y+dy
    done
}

offset_pv=0
offset_inverter=0
offset_battery=0
offset_load=1
offset_grid=0

while true; do
    raw_data=$(curl -s --data-urlencode 'query=holding_register{register=~"31036|31038|31064|31066|31125|31127"}' 'http://192.168.178.104:9090/api/v1/query' | jq -r '.data.result[].value[1]' | tr '\n' ' ')
    declare -a data=(${raw_data})

    value_pv=${data[2]}
    value_soc=${data[1]}
    value_battery=${data[0]}
    value_load=${data[5]}
    value_inverter=${data[4]}
    value_grid=${data[3]}

    let value_battery=value_battery*-1

    # PV Power
    tput cup 2 1
    echo "${value_pv}W   "
    # Inverter Output
    tput cup 12 1
    echo "${value_inverter}W   "
    # Battery SOC
    tput cup 22 1
    echo "${value_soc}%   "
    # Battery Charge Rate
    tput cup 23 1
    echo "${value_battery}W   "
    # Load
    tput cup 12 41
    echo "${value_load}W   "
    # Grid
    tput cup 22 25
    echo "${value_grid}W   "

    # Line PV Power
    animate_line 5 6 5 "down" $offset_pv
    if [ $value_pv -ne 0 ]; then
        let offset_pv=offset_pv-1
    fi

    # Line Inverter
    # animate_line 12 13 17 "right" $offset_inverter
    # let offset_inverter=offset_inverter+1

    # Line Battery
    animate_line 15 6 5 "down" $offset_battery
    if [ $value_battery -gt 0 ]; then
        let offset_battery=offset_battery-1
    elif [ $value_battery -lt 0 ]; then
        let offset_battery=offset_battery+1
    fi

    # Line Inverter
    animate_line 12 13 17 "right" $offset_inverter
    if [ $value_inverter -gt 0 ]; then
        let offset_inverter=offset_inverter-1
    elif [ $value_inverter -lt 0 ]; then
        let offset_inverter=offset_inverter+1
    fi

    # Line Load
    animate_line 12 31 9 "right" $offset_load
    if [ $value_load -gt 0 ]; then
        let offset_load=offset_load-1
    elif [ $value_load -lt 0 ]; then
        let offset_load=offset_load+1
    fi

    # Line Grid
    animate_line 13 30 7 "down" $offset_grid
    if [ $value_grid -gt 0 ]; then
        let offset_grid=offset_grid-1
    elif [ $value_grid -lt 0 ]; then
        let offset_grid=offset_grid+1
    fi

    # test cursor
    # tput cup 12 13
    # echo 'X'

    # put cursor away
    tput cup 25 0

    sleep 0.2
done
