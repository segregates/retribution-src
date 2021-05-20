#!/bin/sh

# Check if it is a symlink. If it is, then sets the correct path so python won't complain.
if [[ -L "${0%/*}" ]]; then
    cd `readlink "${0%/*}"  | xargs dirname | xargs dirname`
else
    cd ..
fi

killall pid of mongod

mongod --dbpath  /data/db  --fork --syslog