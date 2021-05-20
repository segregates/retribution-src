from panda3d.core import lookAt
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.DistributedSmoothNodeBase import DistributedSmoothNodeBase
from direct.distributed.GridParent import GridParent
from direct.distributed.ClockDelta import *
from pirates.battle.DistributedBattleAvatarAI import *
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from EnemyMoverAI import EnemyMoverAI
import random

AvToEnemies = {}

class DistributedBattleNPCAI(DistributedBattleAvatarAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')
    isNpc = True

    def __init__(self, spawner):
        self.spawner = spawner
        DistributedBattleAvatarAI.__init__(self, spawner.air)
        FSM.__init__(self, 'DistributedBattleNPCAI')
        self.spawnPos = (0, 0, 0)
        self.spawnPosIndex = ''
        self.associatedQuests = []

        self.animSet = 'default'
        self.noticeAnim1 = ''
        self.noticeAnim2 = ''
        self.greetingAnim = ''

        self.collisionMode = PiratesGlobals.COLL_MODE_ALL
        self.initZ = 0
        self.uniqueId = ''
        self.dnaId = ''

        self.damageScale = 1
        self.patrolRadius = -1
        self.mover = None
        self.walkLocation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.enemies = []

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def getDNAId(self):
        return self.dnaId

    def getSpawnPos(self):
        return self.spawnPos
        
    def setLevel(self, level):
        if not level:
            level = EnemyGlobals.getRandomEnemyLevel(self.avatarType)
        DistributedBattleAvatarAI.setLevel(self, level)
        maxHp = EnemyGlobals.getMonsterHp(level)
        self.setHp(maxHp)
        self.setMaxHp(maxHp)

    def setPatrolRadius(self, patrolRadius):
        self.patrolRadius = patrolRadius
    
    def getPatrolRadius(self):
        return self.patrolRadius
    
    def hasPatrolRadius(self):
        return self.patrolRadius > 0

    def announceGenerate(self):
        DistributedBattleAvatarAI.announceGenerate(self)
        self.demand('Spawn')

        self.skills = EnemyGlobals.getEnemySkills(self.avatarType, self.level)
        self.weapons = EnemyGlobals.getEnemyWeapons(self.avatarType, self.level)
        
        self.mainWeapon = self.weapons.keys()[0]
        if self.mainWeapon > 1:
            startDrawn = self.animSet in EnemyGlobals.DRAWN_ANIME
            if self.mainWeapon in EnemyGlobals.DRAWN_WEAPONS:
                startDrawn = True
            self.b_setCurrentWeapon(self.mainWeapon, startDrawn)
    
    def b_setWalkLocation(self, walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH):
        self.setWalkLocation(walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH)
        self.d_setWalkLocation(*self.walkLocation)

    def setWalkLocation(self, walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH):
        self.walkLocation = [globalClockDelta.getRealNetworkTime(), walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH]
    
    def d_setWalkLocation(self, timestamp, walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH):
        self.sendUpdate('setWalkLocation', [timestamp, walkTime, rotateTime, sX, sY, sZ, eX, eY, eZ, sH, eH])
    
    def getWalkLocation(self):
        return self.walkLocation

    def enterSpawn(self):
        self.sendUpdate('setSpawnIn', [globalClockDelta.getRealNetworkTime(bits=32)])
        self.addSkillEffect(WeaponGlobals.C_SPAWN)
        taskMgr.doMethodLater(8, self.__removeSpawn, self.uniqueName('spawned'))

    def __removeSpawn(self, task):
        self.removeSkillEffect(WeaponGlobals.C_SPAWN)
        self.demand(self.getStartState())
        return task.done

    def exitSpawn(self):
        taskMgr.remove(self.uniqueName('spawned'))
        self.removeSkillEffect(WeaponGlobals.C_SPAWN)
        self.d_updateSmPos()
    
    def enterOff(self):
        if self.mover:
            self.mover.destroy()
        
        self.mover = None
        self.stopPosHprBroadcast()

    def delete(self):
        self.demand('Off')
        messenger.send('enemyDefeated', [self])
        DistributedBattleAvatarAI.delete(self)

    def setSpawnPos(self, spawnPos):
        self.spawnPos = spawnPos

    def getSpawnPos(self):
        return self.spawnPos

    def getSpawnPosIndex(self):
        # This seems related to quests, return uniqueId for now
        return self.getUniqueId()

    def setAssociatedQuests(self, associatedQuests):
        self.associatedQuests = associatedQuests

    def getAssociatedQuests(self):
        return self.associatedQuests

    def setActorAnims(self, animSet, noticeAnim1, noticeAnim2, greetingAnim):
        self.animSet = animSet
        self.noticeAnim1 = noticeAnim1
        self.noticeAnim2 = noticeAnim2
        self.greetingAnim = greetingAnim

    def getActorAnims(self):
        return [self.animSet, self.noticeAnim1, self.noticeAnim2, self.greetingAnim]

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def getCollisionMode(self):
        return self.collisionMode

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def setAvatarType(self, avatarType):
        DistributedBattleAvatarAI.setAvatarType(self, avatarType)
        self.setName(self.avatarType.getName())

    def getUniqueId(self):
        return self.uniqueId

    # setInitZ is not used by client
    def setInitZ(self, initZ):
        self.initZ = initZ

    def getInitZ(self):
        return self.initZ

    def posControlledByCell(self):
        area = self.getParentObj()

        cell = GridParent.getCellOrigin(area, self.zoneId)
        pos = self.getPos()
        parent = self.getParent()
        self.reparentTo(cell)
        self.setPos(area, pos)
        self.wrtReparentTo(parent)

        self.relativePos = self.getPos(self.getParent())
        self.setWalkLocation(0, 0, self.getX(), self.getY(), self.getZ(), 0, 0, 0, self.getH(), 0)
        self.d_updateSmPos()
        return False

    def d_updateSmHpr(self):
        self.sendUpdate('setSmH', [self.getH(), 0])

    def d_updateSmPos(self):
        x, y, z, h, p, r = list(self.getPos()) + list(self.getHpr())
        self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, 0])

    def enterBattle(self):
        if self.mover:
            self.mover.demand('FollowEnemy')

        self.sendUpdate('setIsAlarmed', [1, self.getAggroRadius()])
        self.waitForNextBattleTask()
        if self.mainWeapon > 1:
            self.b_setCurrentWeapon(self.mainWeapon, 1)

    def enterIdle(self):
        if (not self.mover) and self.hasPatrolRadius() and self.isBattleable() and not self.avatarType.isA(AvatarTypes.FlyTrap):
            self.mover = EnemyMoverAI(self)

        if self.mover:
            self.mover.demand('Wander')
    
    def exitIdle(self):
        if self.mover:
            self.mover.demand('Off')

    def waitForNextBattleTask(self):
        dt = random.random() * 6 + .15
        dt -= self.getLevel() / 25.0
        dt = max(.3, dt)
        taskMgr.doMethodLater(dt, self.__battleTask, self.taskName('battleTask'))

    def __battleTask(self, task):
        remove = []
        parent = self.getParent()

        for enemy in self.enemies:
            av = self.air.doId2do.get(enemy)
            if not av:
                remove.append(enemy)
                continue

            if av.hp <= 0:
                remove.append(enemy)
                continue

            if av.parentId != self.parentId:
                remove.append(enemy)
                continue

            if (self.relativePos - av.getPos(parent)).length() > EnemyGlobals.CALL_FOR_HELP_DISTANCE:
                remove.append(enemy)
                continue

        for r in remove:
            self.removeEnemy(r)

        if not self.enemies:
            if remove:
                self.d_setTaunt(EnemyGlobals.BREAK_COMBAT_CHAT, remove)

            self.demand('Idle')
            return task.done

        target, = random.sample(self.enemies, 1)
        av = self.air.doId2do[target]

        skillId = random.choice(self.skills.keys())
        ammoSkillId = 0 # TO DO
        pos = self.getPos(parent) - av.getPos(parent)
        self.headsUp(av)
        self.d_updateSmHpr()
        result = self.attemptUseTargetedSkill(skillId, ammoSkillId, 0, av.doId, [],
                                              globalClockDelta.getRealNetworkTime(bits=32),
                                              pos, 0)
        if result == WeaponGlobals.RESULT_OUT_OF_RANGE and not ammoSkillId:
            self.removeEnemy(av.doId)
            self.d_setTaunt(EnemyGlobals.BREAK_COMBAT_CHAT, [av.doId])
        elif random.random() > 0.75:
            if self.isTeamTalk(av.doId):
                self.d_setTaunt(EnemyGlobals.TEAM_CHAT, [av.doId])
            else:
                self.d_setTaunt(EnemyGlobals.TAUNT_CHAT, [av.doId])

        self.waitForNextBattleTask()
        return task.done

    def isBattleable(self):
        return 1
        
    def isTeamTalk(self, avId):
        return avId in AvToEnemies and len(AvToEnemies[avId]) > 1

    def setDamageScale(self, damageScale):
        self.damageScale = damageScale

    def getMonsterDmg(self):
        return EnemyGlobals.getMonsterDmg(self.level) * self.damageScale

    def getEnemyPosition(self):
        lastIndex = 0
        
        while lastIndex < len(self.enemies):
            av = self.air.doId2do.get(self.enemies[lastIndex])
            
            if av and av.parentId == self.parentId:
                pos = av.getPos(self.getParent())
                distance = (self.relativePos - pos).length()
                
                if distance <= EnemyGlobals.CALL_FOR_HELP_DISTANCE:
                    if (self.getPos(self.getParent()) - pos).length() <= 3.5:
                        return None
                    else:
                        return pos
            
            lastIndex += 1

    def getFocusingEnemy(self):
        lastIndex = 0
        
        while lastIndex < len(self.enemies):
            av = self.air.doId2do.get(self.enemies[lastIndex])
            
            if av:
                return av
            
            lastIndex += 1

    def exitBattle(self):
        if self.mover:
            self.mover.demand('Off')
    
        self.sendUpdate('setIsAlarmed', [0, 0])
        taskMgr.remove(self.taskName('battleTask'))
        
        if self.mainWeapon > 1:
            endDrawn = self.animSet in EnemyGlobals.DRAWN_ANIME or self.mainWeapon in EnemyGlobals.DRAWN_WEAPONS
            self.b_setCurrentWeapon(self.mainWeapon, endDrawn)

    def d_setTaunt(self, tauntType, avIds):
        taunts = PLocalizer.getEnemyChat(self.avatarType, tauntType)

        if not taunts:
            tauntType = EnemyGlobals.NO_CHAT
            chatId = 0
        else:
            chatId = random.randint(0, len(taunts) - 1)

        self.sendUpdate('setTaunt', [tauntType, chatId, avIds])

    # TO DO:
    # boardVehicle(uint32) broadcast ram
    # setChat(string, uint8) broadcast ownsend
    # requestAnimSet(string) broadcast

    def handleInteract(self, avId, interactType, instant):
        if interactType == PiratesGlobals.INTERACT_TYPE_HOSTILE:
            if avId not in self.enemies:
                av = self.air.doId2do.get(avId)
                
                if (not av):
                    return IGNORE

                pos = av.getPos(self.getParent())
                distance = (self.relativePos - pos).length()
                
                if distance > EnemyGlobals.CALL_FOR_HELP_DISTANCE:
                    return IGNORE

                self.enemies.append(avId)
                self.d_setTaunt(EnemyGlobals.AGGRO_CHAT, [avId])
                av.sendUpdate('setCurrentTarget', [0])

                enemies = AvToEnemies.get(avId, [])
                
                if self.getUniqueId() not in enemies:
                    enemies.append(self.getUniqueId())
                    AvToEnemies[avId] = enemies

            if self.state not in ('Battle', 'Death'):
                self.demand('Battle')

        return IGNORE

    def requestExit(self):
        avId = self.air.getAvatarIdFromSender()
        self.removeEnemy(avId)

    def removeEnemy(self, avId):
        if avId not in self.enemies:
            return

        self.enemies.remove(avId)

        av = self.air.doId2do.get(avId)

        if av:
            av.sendUpdate('setCurrentTarget', [0])

        if avId not in AvToEnemies:
            return

        if not av:
            del AvToEnemies[avId] 
        else: 
            enemies = AvToEnemies[avId]
                    
            if self.getUniqueId() in enemies:
                enemies.remove(self.getUniqueId())
                AvToEnemies[avId] = enemies

    def enterAmbush(self):
        self.sendUpdate('setAmbush', [1])

    def ambushIntroDone(self):
        if self.state == 'Ambush':
            self.demand('Battle')

    def died(self):
        self.demand('Death')

    def enterDeath(self):
        def doDeath(task):
            self.spawner.died()
            self.requestDelete()
            return task.done

        self.applyRewards()

        if self.air.lootManager:
            self.air.lootManager.spawnLoot(self)

        messenger.send('enemyDefeated', [self])
        taskMgr.doMethodLater(5, doDeath, self.taskName('death'))

    def applyRewards(self):
        multiplier = random.randint(6, 12) / 1.2
        for avId, skills in self.enemySkills.items():
            av = self.air.doId2do.get(avId)
            if not av:
                continue

            repId2rep = {}
            for repId, skillId, ammoSkillId in skills:
                amount = int(self.level * WeaponGlobals.getAttackReputation(skillId, ammoSkillId) * multiplier)
                repId2rep[repId] = repId2rep.get(repId, 0) + amount

            for repId, amount in repId2rep.items():
                while amount > 125:
                    amount = int(amount / 1.173)
                av.addReputation(repId, amount)

            av.repChanged()

    def exitDeath(self):
        taskMgr.remove(self.taskName('death'))

    def demand(self, state, *args):
        FSM.demand(self, state, *args)
        self.sendUpdate('setGameState', [state, globalClockDelta.getRealNetworkTime()])
    
    def requestClientAggro(self):
        avId = self.air.getAvatarIdFromSender()
        
        self.handleInteract(avId, PiratesGlobals.INTERACT_TYPE_HOSTILE, 0)

    @staticmethod
    def makeFromObjectKey(cls, spawner, uid, avType, data):
        if cls is None:
            cls = DistributedBattleNPCAI

        obj = cls(spawner)

        x, y, z = data.get('Pos', (0, 0, 0))
        h, p, r = data.get('Hpr', (0, 0, 0))
        pos = (x, y, z)
        hpr = (h, p, r)

        gridPos = data.get('GridPos')
        if gridPos:
            pos = gridPos

        obj.setSpawnPos(pos)
        obj.setPos(pos)
        obj.setHpr(hpr)

        animSet = data.get('AnimSet', 'default')
        noticeAnim1 = data.get('Notice Animation 1', '')
        noticeAnim2 = data.get('Notice Animation 2', '')
        greetingAnim = data.get('Greeting Animation', '')

        obj.setAvatarType(avType)
        obj.setUniqueId(uid)
        obj.setActorAnims(animSet, noticeAnim1, noticeAnim2, greetingAnim)
        try:
            obj.setIsGhost(int(data['GhostFX']))
        except:
            # some objects don't have GhostFX declared in their data.
            obj.setIsGhost(0)
        try:
            obj.setGhostColor(int(data['GhostColor']))
        except:
            obj.setGhostColor(0)
            
        if 'Level' in data:
            level = data['Level']
            
            if isinstance(level, list):
                level = random.choice(level)

            obj.setLevel(int(level))
        
        if 'Patrol Radius' in data:
            obj.setPatrolRadius(float(data['Patrol Radius']))

        if 'Aggro Radius' in data:
            obj.setAggroRadius(int(float(data['Aggro Radius'])))

        if 'Start State' in data:
            state = data['Start State']

            if state in ('Walk', 'Patrol'):
                state = 'Idle'

            obj.setStartState(state)
        return obj
