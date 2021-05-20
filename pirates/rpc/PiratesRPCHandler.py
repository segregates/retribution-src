from pirates.rpc.PiratesRPCHandlerBase import *
from otp.distributed import OtpDoGlobals
from otp.ai.BanManagerAI import BanManagerAI

from pirates.distributed.ShardStatusReceiver import ShardStatusReceiver

class PiratesRPCHandler(PiratesRPCHandlerBase):
    def __init__(self, air):
        PiratesRPCHandlerBase.__init__(self, air)
        self.shardStatus = ShardStatusReceiver(self.air)
        self.banMgr = BanManagerAI(self.air)

    # --- TESTING ---
    @rpcmethod(CATEGORY_ANY, args={'data': 'string'})
    def rpc_ping(self, callback, data):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.

        Parameters:
            [any data] = The data to be given back in response.

        Example response: 'pong'
        """
        callback(data)

    # --- GENERAL ---
    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'doId': 'int'})
    def rpc_queryObject(self, callback, doId):
        """
        Summary:
            Responds with the values of all database fields associated with the
            provided [doId].

        Parameters:
            [int doId] = The ID of the object to query database fields on.

        Example response:
            On success: ['DistributedObject', {'fieldName': ('arg1', ...), ...}]
            On failure: [None, None]
        """
        def _callback(dclass, fields):
            if dclass is not None:
                dclass = dclass.getName()
            callback([dclass, fields])

        self.air.dbInterface.queryObject(self.air.dbId, doId, _callback)

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'doId': 'int', 'dclassName': 'string',
                                                 'newFields': 'dict', 'oldFields': 'dict'})
    def rpc_updateObject(self, callback, doId, dclassName, newFields, oldFields=None):
        """
        Summary:
            Update the field(s) of the object associated with the provided
            [doId]. If <oldFields> is provided, then this method will fail if
            the object's current fields don't match.

        Parameters:
            [int doId] = The ID of the object whose fields are to be updated.
            [str dclassName] = The name of the object's DClass.
            [dict newFields] = The new field values.
            <dict oldFields> = The old field values to assert.

        Example response:
            On success: True
            On failure: False
        """
        # Ensure that the provided DClass exists:
        if dclassName not in self.air.dclassesByName:
            dclassName += 'UD'
            if dclassName not in self.air.dclassesByName:
                callback(False)

        dclass = self.air.dclassesByName[dclassName]

        if oldFields is None:
            self.air.dbInterface.updateObject(
                self.air.dbId, doId, dclass, newFields)
            callback(True)

        def callback(fields):
            callback(fields is None)

        self.air.dbInterface.updateObject(
            self.air.dbId, doId, dclass, newFields, oldFields=oldFields,
            callback=callback)

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'doId': 'int', 'dclassName': 'string', 'args': 'list'})
    def rpc_setField(self, callback, doId, dclassName, fieldName, args=[]):
        """
        Summary:
            Set the value of the field named [fieldName] on the suggested
            object.

        Parameters:
            [int doId] = The ID of the object whose field is being modified.
            [str dclassName] = The name of the object's DClass.
            [str fieldName] = The name of the field to be modified.
            [list args] = The new value for the field.

        Example response:
            On success: True
            On failure: False
        """
        # Ensure that the provided DClass exists:
        if dclassName not in self.air.dclassesByName:
            dclassName += 'UD'
            if dclassName not in self.air.dclassesByName:
                callback(False)

        dclass = self.air.dclassesByName[dclassName]

        datagram = dclass.aiFormatUpdate(
            fieldName, doId, doId, self.air.ourChannel, args)
        self.air.send(datagram)

        callback(True)

    # --- SHARD MANAGEMENT --- #
    @rpcmethod(CATEGORY_GAME_DEVELOPER, args={'districtId': 'int'})
    def rpc_closeDistrict(self, callback, districtId):
        """
        Summary:
            Sets a district to unavailable, by [districtId].
        """
        dclass = self.air.dclassesByName['PiratesDistrictAI']
        dg = dclass.aiFormatUpdate('rpcSetAvailable', districtId, districtId,
                                    self.air.ourChannel, [0])
        self.air.send(dg)
        callback(None)

    @rpcmethod(CATEGORY_ANY, args={})
    def rpc_listShards(self, callback):
        """
        Summary:
            Responds with the current status of each shard that has ever been
            created in the lifetime of the UberDOG.

        Example response:
            {
               401000000: {
                  'name': 'District Name'
                  'available': True,
                  'created': 1409665000,
                  'population': 150,
                  'invasion': {
                     'type': 'Jolly Roger Bay',
                     'flags': 0,
                     'remaining': 1000,
                     'total': 1000,
                     'start': 1409665000
                  }
               },
               ...
            }
        """
        callback(self.shardStatus.getShards())

    # --- KICK --- ###
    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'channel': 'int', 'code': 'int', 'reason': 'string'})
    def rpc_kickChannel(self, callback, channel, code=155, reason="No reason has been specified."):
        """
        Summary:
            Kicks any users whose CAs are subscribed to a particular [channel] with a [code].

        Parameters:
            [int channel] = The channel to direct the message to.
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """
        self.banMgr.kickChannel(channel, code, reason)
        callback(None)

    @rpcmethod(CATEGORY_MODERATION, args={'avId': 'int', 'code': 'int', 'reason': 'string'})
    def rpc_kickAvatar(self, callback, avId, code=155, reason="No reason has been specified."):
        """
        Summary:
            Kicks a particular [avId].

        Parameters:
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """
        self.banMgr.kickAvatar(callback, avId, code, reason) # Calls callback

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'code': 'int', 'reason': 'string'})
    def rpc_kickAll(self, callback, code=155, reason="No reason has been specified."):
        """
        Summary:
            Kicks every user on the game.

        Parameters:
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """

        channel = 10 # The Astron "all clients" channel.
        return self.rpc_kickChannel(callback, channel, code, reason) # Calls callback

    # --- MESSAGING --- #
    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'channel': 'int', 'message': 'string'})
    def rpc_messageChannel(self, callback, channel, message):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """
        self.air.systemMessage(message, channel)
        callback(None)

    @rpcmethod(CATEGORY_MODERATION, args={'avId': 'int', 'message': 'string'})
    def rpc_messageAvatar(self, callback, avId, message):
        """
        Summary:
            Broadcasts a [message] to a specific [avId] (user).

        Parameters:
        [str message] = The message to broadcast.
        """

        channel = avId + (1001L << 32)
        return self.rpc_messageChannel(channel, message) # Calls callback

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'message': 'string'})
    def rpc_messageAll(self, callback, message):
        """
        Summary:
            Broadcasts a [message] to the entire server globally.

        Parameters:
        [str message] = The message to broadcast.
        """

        channel = 10 # The Astron "all clients" channel.
        return self.rpc_messageChannel(callback, channel, message) # Calls callback

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'message': 'string'})
    def rpc_messageAllAdmin(self, callback, message):
        """
        Summary:
            Broadcasts a [message] to the entire server globally with the admin prefix.

        Parameters:
        [str message] = The message to broadcast.
        """

        message = "ADMIN: " + message
        return self.rpc_messageAll(callback, message) # Calls callback

    @rpcmethod(CATEGORY_SYSTEM_ADMINISTRATOR, args={'reason': 'string'})
    def rpc_update(self, callback, reason="for an update"):
        """
        Summary:
            Alerts all users of POR shutting down for maintenance with optional [reason].
        """
        message = 'Ahoy, maties! Pirates Online Retribution will be closing momentarily %s.' % reason
        return self.rpc_messageAllAdmin(callback, message) # Calls callback
