

class TalkMessage:

    def __init__(self, talkType, messageId, body, senderAvatarId=None, senderAvatarName=None, receiverAvatarId=None, receiverAvatarName=None, extraInfo=None):
        self.body = body
        self.senderAvatarId = senderAvatarId
        self.senderAvatarName = senderAvatarName
        self.receiverAvatarId = receiverAvatarId
        self.receiverAvatarName = receiverAvatarName
        self.talkType = talkType
        self.extraInfo = extraInfo
        self.messageId = messageId

    def getMessageId(self):
        return self.messageId

    def setMessageId(self, id):
        self.messageId = id

    def getBody(self):
        return self.body

    def setBody(self, body):
        self.body = body

    def getSenderAvatarId(self):
        return self.senderAvatarId

    def setSenderAvatarId(self, senderAvatarId):
        self.senderAvatarId = senderAvatarId

    def getSenderAvatarName(self):
        return self.senderAvatarName

    def setSenderAvatarName(self, senderAvatarName):
        self.senderAvatarName = senderAvatarName

    def getReceiverAvatarId(self):
        return self.receiverAvatarId

    def setReceiverAvatarId(self, receiverAvatarId):
        self.receiverAvatarId = receiverAvatarId

    def getReceiverAvatarName(self):
        return self.receiverAvatarName

    def setReceiverAvatarName(self, receiverAvatarName):
        self.receiverAvatarName = receiverAvatarName

    def getTalkType(self):
        return self.talkType

    def setTalkType(self, talkType):
        self.talkType = talkType

    def getExtraInfo(self):
        return self.extraInfo

    def setExtraInfo(self, extraInfo):
        self.extraInfo = extraInfo
