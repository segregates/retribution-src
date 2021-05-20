# STUB

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedCrewMatchManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    # requestCrewAdd(uint8, uint32, uint32, uint32, uint32, uint32) airecv clsend

    # requestCrewAddUD(uint32, string, uint8, string, uint32, uint8, uint32, uint32, uint8, bool, uint32, uint32, uint32)

    # responseCrewAdd(int8)

    # requestCrewDelete() airecv clsend

    # requestCrewDeleteUD(uint32)

    # responseCrewDelete(uint8)

    # requestCrewUpdate(uint32, uint8, string, uint32)

    # requestCrewChangeOptions(uint8, uint32, uint32) airecv clsend

    # addBandMember(uint32, uint32, uint32, uint32, uint8)

    # removeAvatarFromLookoutList(uint32)

    # removeCrewFromLookoutList(uint32)

    # requestInitialAvatarAdd(uint8) airecv clsend

    # requestInitialAvatarAddUD(uint32, string, uint8, uint32, uint32, uint8, uint32)

    # responseInitialAvatarAdd(uint8, string, uint32, string, uint8)

    # requestInitialAvatarAddResponse(uint8, uint8) airecv clsend

    # responseInitialAvatarAddResponse(uint8)

    # requestPutAvatarOnLookoutList(uint8) airecv clsend

    # requestPutAvatarOnLookoutListUD(uint32, string, uint8, uint32, uint32, uint8, uint32)

    # requestDeleteAvatarFromLookoutList() airecv clsend

    # requestDeleteAvatarFromLookoutListUD(uint32) airecv clsend

    # responseCrewFound(string, uint32, string)

    # responseCrewGone()

    # requestAcceptInvite(uint32) airecv clsend

    # requestCrewOfOneCreation() airecv clsend

    # requestCrewOfOneDelete() airecv clsend

    # notifySponsorNewMember(uint32, string)

    # responseNewMemberRequest(uint32, string, uint8, uint32)

    # requestNewMember(uint32, uint8, uint8, uint32) airecv clsend

    # notifyNewMemberAskingCrewLeader(uint32, string)

    # notifyNewMemberAccept(uint32, string)

    # notifyNewMemberDecline(uint32, string)

    # notifyNewMemberTeleport(uint32, string)

    # notifyNewMemberTeleportToNewShard(uint32, string, uint32, uint32, uint32)

    # requestTeleportQuery(uint32, uint32, uint32, uint32, uint32) airecv clsend

    # requestTeleportResponse(uint32, int8, uint32, uint32, uint32) airecv clsend

    # teleportQuery(uint32, uint32, uint32, uint32, uint32) airecv clsend

    # teleportResponse(uint32, int8, uint32, uint32, uint32) airecv clsend


