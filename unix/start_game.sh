#!/bin/sh

#Use thie file to use the game on Mac/Linux

# Check if it is a symlink. If it is, then sets the correct path so python won't complain.
if [[ -L "${0%/*}" ]]; then
    cd `readlink "${0%/*}"  | xargs dirname | xargs dirname`
else
    cd ..
fi

read -p "Username: " POR_PLAYCOOKIE
read -p "Gameserver: " POR_GAMESERVER

echo "=============================="
echo "Starting Pirates Online..."
echo "Username: $POR_PLAYCOOKIE"
echo "Gameserver: $POR_GAMESERVER"
echo "=============================="

ppython -m pirates.piratesbase.PiratesStartDev