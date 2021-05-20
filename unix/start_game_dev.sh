#!/bin/sh

#Use thie file to use the game on Mac/Linux

# Check if it is a symlink. If it is, then sets the correct path so python won't complain.
if [[ -L "${0%/*}" ]]; then
	cd `readlink "${0%/*}"  | xargs dirname | xargs dirname`
else
	cd ..
fi

$POL_PLAYCOOKIE #read -p "Username: " $POL_PLAYCOOKIE
$POL_GAMESERVER #read -p "Gameserver: " $POL_GAMESERVER

echo "=============================="
echo "Starting Pirates Online Legacy..."
echo "Username: $POL_PLAYCOOKIE"
echo "Gameserver: $POL_GAMESERVER"
echo "=============================="

ppython -m pirates.piratesbase.PiratesStartDev