Pirates Online Retribution Source Code
======================================


CANT GET RID OF THE LEAK FOR LONG CAN YOU?

Why dont you just close your shit server?


This repository is the source code for Pirates Online Retribution.

## Build Instructions
Instrutions on how to set up a development environment for POR (run server/clients locally)

#### 1) Install Git and learn the basics

#### 2) Panda3D




Move the P3D from this directory to C:/

#### 3) Install MongoDB

From here: https://www.mongodb.com/download-center?jmp=nav



Run this to make the appropriate folder structure for it, or just make them manually.

mkdir C:/data



mkdir C:/data/db



#### 4) Test the server/client



Go to `win32` if you're on Windows and double click `start-all.bat`.

### Rules

*  Push the game code to any repository you want.
* *Always* force a git push.

### Production

**LIVE**: In production, we will be using git tags for deployment on the master branch. When we are ready to deploy a prod build, we will merge qa into master and then create a git tag. 

**QA**: Deployment is based on git commit hashes using the qa branch.
Note: Currently unused, just push to master.



---

**These are a list of crashlogs submitted to us by players on the public server. If a crash has been fixed/resolved, insert a (RESOLVED) following the description for the crash and the link to it. We'd like to keep all of these crashes on record, so do not remove any of them.**


1.) Very bumpy crash, not responding, then not working, then closed program, it responds and plays for 3 seconds, then closes.
https://cdn.discordapp.com/attachments/226498380338167808/228280686304428033/160921_171726.log

2.) Memory Leak - https://tohka.us/i/Cen0BQui.png

3.) was fighting an alligator on tortuga, alligator wasn't taking damage then I lost connection to the server - https://cdn.discordapp.com/attachments/227515252252737536/228283977763389441/unknown.png

4.) I threw a grenade at an alligator and it crashed - https://cdn.discordapp.com/attachments/225307184487989248/228286681143443456/160921_183452.log

5.) I just crashed on Tortuga while shooting an alligator - https://cdn.discordapp.com/attachments/228287346183766018/228291381385363458/nativelog.txt

6.) Been getting this whenever I initiate a fight - http://pastebin.com/6nrTvs8q

7.) When using a particular weapon - http://pastebin.com/de6meaTG

8.) trying to put a weapon in one of the weapon slots - http://pastebin.com/fPTCxBUe

9.) This is happening frequently while fishing - http://prntscr.com/ckwduw

10.) I was in the graveyard, fighting the undead enemies. - https://cdn.discordapp.com/attachments/228424497882071041/228425345064370176/160922_035255.log


