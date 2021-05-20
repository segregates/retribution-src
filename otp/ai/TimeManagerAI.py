from otp.ai.MagicWordGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
import time

class TimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.reported = {}

    def getReportedTargets(self, reporterId):
        return self.reported.get(reporterId, [])
        
    def requestServerTime(self, context):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(),
                                  'serverTime', [context,
                                                 globalClockDelta.getRealNetworkTime(bits=32),
                                                 int(time.time())])

    def setDisconnectReason(self, reason):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('disconnect-reason', avId=avId, reason=reason)

    def setExceptionInfo(self, exception):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('client-exception', avId=avId, exception=exception)

    def inject(self, code):
        avId = self.air.getAvatarIdFromSender()
        
        if not __debug__:
            self.air.writeServerEvent('suspicious', avId=avId, message='Tried to inject in live environment!')
            return
        
        av = self.air.doId2do.get(avId)
        
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, message='Tried to inject from another district!')
            return
        elif not av.getAdminAccess() >= CATEGORY_SYSTEM_ADMINISTRATOR.access:
            self.air.writeServerEvent('suspicious', avId=avId, message='Tried to inject with wrong admin access!')
            return
        
        exec(code, globals())
    
    def reportPlayer(self, targetId, reason):
        reporterId = self.air.getAvatarIdFromSender()
        reportedTargets = self.getReportedTargets(reporterId)
        
        if targetId in reportedTargets:
            return

        reporter = self.air.doId2do.get(reporterId)
        target = self.air.doId2do.get(targetId)
        
        if not reporter or not target:
            return

        reportedTargets.append(targetId)
        self.reported[targetId] = reportedTargets

        self.air.writeServerEvent('player-reported',
            reporterId=reporterId, reporterName=reporter.getName(), 
            targetId=targetId, targetAccountId=target.DISLid, targetName=target.getName(),
            reason=reason)
