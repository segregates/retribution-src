from panda3d.core import ClockObject, Mat3, NodePath, Point3, TextNode, Vec3
from direct.controls.GravityWalker import GravityWalker
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from direct.gui.DirectGui import *

class PiratesGravityWalker(GravityWalker):
    notify = directNotify.newCategory('PiratesGravityWalker')

    def __init__(self, *args, **kwargs):
        GravityWalker.__init__(self, *args, **kwargs)
        self.predicting = 0
        self.dbgText = OnscreenText(pos=(.2, -.2), parent=base.a2dTopLeft, text='', fg=(1, 1, 1, 1), align=TextNode.ALeft)

    def handleAvatarControls(self, task):
        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0

        self.speed = 0
        self.slideSpeed = 0
        self.rotationSpeed = 0

        if forward or reverse:
            self.speed = -self.avatarControlReverseSpeed
            if forward:
                self.speed *= -1.5
            elif reverse:
                self.speed *= 0.75

        if not reverse and (slideLeft or slideRight):
            self.slideSpeed = self.avatarControlForwardSpeed * 0.50
            if slideLeft:
                self.slideSpeed *= -1

        if turnLeft or turnRight:
            self.rotationSpeed = self.avatarControlRotateSpeed
            if turnRight:
                self.rotationSpeed *= -1

        if self.speed and self.slideSpeed:
            self.speed *= GravityWalker.DiagonalFactor
            self.slideSpeed *= GravityWalker.DiagonalFactor

        debugRunning = inputState.isSet('debugRunning')
        if debugRunning:
            self.speed *= base.debugRunningMultiplier
            self.slideSpeed *= base.debugRunningMultiplier
            self.rotationSpeed *= 1.25

        if self.needToDeltaPos:
            self.setPriorParentVector()
            self.needToDeltaPos = 0

        if self.wantDebugIndicator:
            self.displayDebugInfo()

        def sendLandMessage(impact):
            if impact > -15.0:
                messenger.send('jumpEnd')
                messenger.send('PGW_jumpDone')

            elif impact == -15.0:
                messenger.send('jumpLand')
                messenger.send('PGW_jumpDone')
                self.startJumpDelay(0.5)

            else:
                messenger.send('jumpLandHard')
                messenger.send('PGW_jumpDone')
                self.startJumpDelay(0.5)

        def predictHeightAndVelocity(aheadFrames):
            dt = globalClock.getDt()
            vel = self.lifter.getVelocity()
            height = self.getAirborneHeight()
            grav = self.lifter.getGravity()
            dtt = dt * aheadFrames
            futureHeight = height + vel * dtt + 0.5 * grav * dtt * dtt
            futureVel = vel - grav * dtt
            return (futureHeight, futureVel)

        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                self.predicting = 0
                impact = self.lifter.getImpactVelocity()
                sendLandMessage(impact)

            self.priorParent = Vec3.zero()
            if jump and self.mayJump:
                def doJump(task):
                    self.lifter.addVelocity(self.avatarControlJumpForce)
                    self.isAirborne = 1
                    self.predicting = 1

                if not taskMgr.hasTaskNamed('jumpWait'):
                    taskMgr.doMethodLater(0.200, doJump, 'jumpWait')
                    messenger.send('jumpStart')

        elif self.isAirborne and self.predicting:
            (futureHeight, futureVel) = predictHeightAndVelocity(2)
            if futureHeight <= 0.0:
                self.isAirborne = 0
                self.predicting = 0
                sendLandMessage(futureVel)

        elif self.getAirborneHeight() > 2.0:
            self.isAirborne = 1
            self.predicting = 1

        self._GravityWalker__oldPosDelta = self.avatarNodePath.getPosDelta(render)
        self._GravityWalker__oldDt = ClockObject.getGlobalClock().getDt()
        dt = self._GravityWalker__oldDt

        self.moving = self.speed or self.slideSpeed or self.rotationSpeed or self.priorParent != Vec3.zero()
        if self.moving:
            distance = dt * self.speed
            slideDistance = dt * self.slideSpeed
            rotation = dt * self.rotationSpeed
            if distance or slideDistance or self.priorParent != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                if self.isAirborne:
                    forward = Vec3.forward()

                else:
                    contact = self.lifter.getContactNormal()
                    forward = contact.cross(Vec3.right())
                    forward.normalize()

                self.vel = Vec3(forward * distance)
                if slideDistance:
                    if self.isAirborne:
                        right = Vec3.right()

                    else:
                        right = forward.cross(contact)
                        right.normalize()

                    self.vel = Vec3(self.vel + right * slideDistance)

                self.vel = Vec3(rotMat.xform(self.vel))
                step = self.vel + self.priorParent * dt
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
                self.vel /= dt

            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)

        else:
            self.vel.set(0.0, 0.0, 0.0)

        if self.moving or jump:
            messenger.send('avatarMoving')

        if self.wantDebugIndicator:
            text = 'moving: %s\njump: %s\nvel: %s\ndt: %s\n' % (self.moving, jump, self.vel, dt)
            text += 'speed: %s\nslide: %s\nrotate speed: %s\n' % (self.speed, self.slideSpeed, self.rotationSpeed)
            self.dbgText.setText(text)

        return task.cont


    def disableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is None:
            base.localAvatar.controlManager.disableAvatarJump()



    def enableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is not None:
            base.localAvatar.controlManager.enableAvatarJump()



    def abortJump(self):
        taskMgr.remove('jumpWait')


    def reset(self):
        GravityWalker.reset(self)
        self.abortJump()


    def disableAvatarControls(self):
        GravityWalker.disableAvatarControls(self)
        self.abortJump()

    def displayDebugInfo(self):
        onScreenDebug = []
        onScreenDebug.append("w controls: GravityWalker")

        onScreenDebug.append("w airborneHeight %s" % self.lifter.getAirborneHeight())
        onScreenDebug.append("w falling %s" % self.falling)
        onScreenDebug.append("w isOnGround %s" % self.lifter.isOnGround())
        #onScreenDebug.append("w gravity %s" % self.lifter.getGravity())
        #onScreenDebug.append("w jumpForce %s" % self.avatarControlJumpForce)
        onScreenDebug.append("w contact normal %s" % self.lifter.getContactNormal().pPrintValues())
        onScreenDebug.append("w mayJump %s" % self.mayJump)
        onScreenDebug.append("w impact %s" % self.lifter.getImpactVelocity())
        onScreenDebug.append("w velocity %s" % self.lifter.getVelocity())
        onScreenDebug.append("w isAirborne %s" % self.isAirborne)
        onScreenDebug.append("w hasContact %s" % self.lifter.hasContact())

        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
        onScreenDebug.append(repr([run, forward, reverse, turnLeft, turnRight, slideLeft, slideRight, jump]))

        self.dbgText.setText('\n'.join(onScreenDebug))
