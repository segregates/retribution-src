#!/bin/sh

#kill process if it is already running
#kill -9  `pgrep -f "pirates.uberdog.ServiceStart"`
pid=$(pgrep -f "pirates.uberdog.ServiceStart")

if [[ $pid ]]; then
    kill -9  $pid
fi




export MAX_CHANNELS=999999
export STATESERVER=1100
export ASTRON_IP=127.0.0.1:29170
export EVENTLOGGER_IP=127.0.0.1:29160
export BASE_CHANNEL=1000000


#start ai server
python -m pirates.uberdog.ServiceStart --base-channel $BASE_CHANNEL --max-channels $MAX_CHANNELS --stateserver $STATESERVER --astron-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP  > logs/uberdog.log 2>&1 &

echo "Pirates Online uberdog server - Process ID#" `pgrep -f "pirates.uberdog.ServiceStart"` - - see log: logs/uberdog.log

echo Starting POR UberDOG server...
echo Base channel: $BASE_CHANNEL
echo Max channels: $MAX_CHANNELS
echo State Server: $STATESERVER
echo Astron IP: $ASTRON_IP
echo Event Logger IP: $EVENTLOGGER_IP

echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="



