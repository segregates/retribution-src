@echo off
title POR AI

set MAX_CHANNELS=999999
set STATESERVER=1100
set ASTRON_IP=127.0.0.1:29170
set EVENTLOGGER_IP=25.127.0.0.1:29160

set DISTRICT_NAME=Davylore
title POR AI - %DISTRICT_NAME%
set BASE_CHANNEL=401000000

echo ===============================
echo Starting POR AI server...
echo District name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

cd ../

:main
"C:\Panda3D-1.10.0\python\ppython.exe" ^
	-m pirates.ai.ServiceStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--astron-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP% ^
	--district-name "%DISTRICT_NAME%"
goto main
