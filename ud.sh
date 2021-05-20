#!/bin/bash

ppython -m pirates.uberdog.ServiceStart --base-channel 1000000 --max-channels 999999 --stateserver 1100 --astron-ip 127.0.0.1:29170 --eventlogger-ip 127.0.0.1:29160 > logs/ud.log 2>&1 &