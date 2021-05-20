@echo off
title TCP Buffer Increase
cls
echo Setting TCP autotune to normal. Please Wait...
netsh interface tcp set global autotuninglevel=normal
echo Importing registry values. Please Wait...
regedit /S tcpbuffersize.reg
echo Import Complete. Please reboot.
pause
