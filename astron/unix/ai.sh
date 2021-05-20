#!/bin/sh

#if you get an exception "No module named pymongo", install pymongo.
# python -m pip install pymongo

#kill process if it is already running
pid=$(pgrep -f "pirates.ai.ServiceStart")

if [[ $pid ]]; then
    kill -9  $pid
fi

export MAX_CHANNELS=999999
export STATESERVER=1100
export ASTRON_IP=127.0.0.1:29170
export EVENTLOGGER_IP=127.0.0.1:29160

export DISTRICT_NAME=Davylore
export title="POR AI - $DISTRICT_NAME"
export BASE_CHANNEL=401000000




#start ai server
python -m pirates.ai.ServiceStart --base-channel $BASE_CHANNEL --max-channels $MAX_CHANNELS --stateserver $STATESERVER --astron-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP --district-name "$DISTRICT_NAME" > logs/ai_server.log 2>&1 &

echo "Pirates Online AI server - Process ID#" `pgrep -f "pirates.ai.ServiceStart"`  - see log: logs/ai_server.log

echo District name: $DISTRICT_NAME
echo Base channel: $BASE_CHANNEL
echo Max channels: $MAX_CHANNELS
echo State Server: $STATESERVER
echo Astron IP: $ASTRON_IP
echo Event Logger IP: $EVENTLOGGER_IP

echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="



