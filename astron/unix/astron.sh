#!/bin/sh

#kill process if it is already running
pid=$(pgrep -f "astron")

if [[ $pid ]]; then
    kill -9  $pid
fi

#start ai server
if [[ "$(uname)" == "Darwin" ]]; then
    #Mac OS X platform
    astron/astrondmac2 --loglevel info astron/config/cluster_yaml.yml  > logs/astron.log 2>&1 &

elif [[  $(uname) =~ ^Linux$ ]]; then
    #GNU/Linux platform
    astron/astrondlinux --loglevel info astron/config/cluster.yml  > logs/astron.log 2>&1 &
fi

echo "Astron - Process ID#" `pgrep -f "astron"`  see log: logs/astron.log
echo "Need to Update the .yml config file to use mongodb!!! - currently using yaml."
echo "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="







