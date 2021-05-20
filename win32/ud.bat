@echo off
title POR UD

set MAX_CHANNELS=999999
set STATESERVER=1100
set ASTRON_IP=127.0.0.1:29170
set EVENTLOGGER_IP=127.0.0.1:29160

set BASE_CHANNEL=1000000

echo ===============================
echo Starting POR UberDOG server...
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

cd ../

:main
"C:\Panda3D-1.10.0\python\ppython.exe" ^
	-m pirates.uberdog.ServiceStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--astron-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%
goto main