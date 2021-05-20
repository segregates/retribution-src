from panda3d.core import Datagram
from direct.distributed.DistributedObjectAI import *
from direct.distributed.PyDatagram import *
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *

class BanManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')

    def __init__(self, air):
        self.air = air

    def kickChannel(self, channel, code=155, reason='No reason has been specificed.'):
        datagram = PyDatagram()
        datagram.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString('You were kicked by a moderator for the following reason:\n\n%s' % reason)
        self.air.send(datagram)

    def kickAccount(self, accountId, code=155, reason='No reason has been specificed.'):
        self.kickChannel(self.GetAccountConnectionChannel(accountId), code, reason)

    def kickAvatar(self, avId, code=155, reason='No reason has been specificed.'):
        self.kickChannel(self.GetPuppetConnectionChannel(avId), code, reason)

    def ban(self, banner, target, time, reason):
        self.air.sendNetEvent('BANMGR_ban', [banner, target.doId, target.DISLid, time, reason])
    
    def mute(self, banner, target, time):
        self.air.sendNetEvent('BANMGR_mute', [banner, target.doId, target.DISLid, time])
    
    def banAI(self, target, time, reason):
        self.air.sendNetEvent('BANMGR_banAI', [target.doId, target.DISLid, time, reason])

@magicWord(category=CATEGORY_GAME_MASTER, types=[str])
def kick(reason='No reason has been specificed.'):
    """Kicks the target user with an optional reason."""
    invoker = spellbook.getInvoker()
    target = spellbook.getTarget()

    if target == invoker:
        return "You can't kick yourself!"

    target.air.banMgr.kickAvatar(target.doId, reason=reason)
    target.air.writeServerEvent('kicked', kickerId=invoker.doId, kickerName=invoker.getName(), reason=reason, targetId=target.doId, targetName=target.getName())
    return 'Kicked %s from the game server!' % target.getName()

@magicWord(category=CATEGORY_GAME_MASTER, types=[int, str])
def ban(hours, reason):
    """Bans the target user with an optional reason."""
    invoker = spellbook.getInvoker()
    target = spellbook.getTarget()

    if target == invoker:
        return 'You cannot ban yourself!'
    
    access = invoker.getAdminAccess()
    
    if access >= CATEGORY_GAME_MASTER.access:
        MAX_TIME = 24 * 60 # 60 days
    else:
        MAX_TIME = 24 * 7 # 7 days
    
    if hours == 0 and access < CATEGORY_GAME_MASTER.access:
        return 'You cannot terminate players!'
    if hours > MAX_TIME:
        return 'You can only ban up to %d hours! Consider terminating! (hours = 0)' % MAX_TIME
    if len(reason) < 3:
        return 'Reason too short!'
    if len(reason) > 32:
        return 'Reason too long (max 32 chars)!'

    target.air.banMgr.ban(invoker.doId, target, hours, reason)

@magicWord(category=CATEGORY_GAME_MASTER, types=[int, str])
def mute(hours):
    """Mutes the target user."""
    invoker = spellbook.getInvoker()
    target = spellbook.getTarget()

    if target == invoker:
        return 'You cannot mute yourself!'
    
    access = invoker.getAdminAccess()
    
    if access >= CATEGORY_GAME_MASTER.access:
        MAX_TIME = 24 * 60 # 60 days
    else:
        MAX_TIME = 24 * 7 # 7 days
    
    if hours == 1 and access < CATEGORY_GAME_MASTER.access:
        return 'You cannot mute players forever!'
    if hours > MAX_TIME:
        return 'You can only mute up to %d hours! Consider muting forever! (hours = 1)' % MAX_TIME

    target.air.banMgr.mute(invoker.doId, target, hours)

@magicWord(category=CATEGORY_GAME_MASTER)
def badName():
    av = spellbook.getTarget()
    oldname = av.name
    av.b_setName('Pirate')
    av.sendUpdate('WishNameState', ['REJECTED'])
    return 'Revoked %s\'s name successfully. They have been renamed to Pirate.' % oldname
