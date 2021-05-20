from pirates.distributed.PiratesDistrictAI import PiratesDistrictAI
from pirates.distributed.PiratesDistrictStatsAI import PiratesDistrictStatsAI
from otp.distributed import OtpDoGlobals
from pirates.piratesbase import PiratesGlobals

class DistrictManagerAI:
    POP_MIN = 1
    POP_MAX = 50

    def __init__(self, air):
        self.air = air

        self.population = 0

        self.district = None
        self.districtStats = None

    def generateDistrict(self):
        self.district = PiratesDistrictAI(self.air)
        self.district.setName(self.air.districtName)
        self.district.generateWithRequiredAndId(
            self.air.districtId, OtpDoGlobals.OTP_DO_ID_PIRATES, 2
        )
        
        self.districtStats = PiratesDistrictStatsAI(self.air)
        self.districtStats.setPiratesDistrictId(self.air.districtId)
        self.districtStats.generateWithRequiredAndId(self.air.allocateChannel(), OtpDoGlobals.OTP_DO_ID_PIRATES, 3)

    def openDistrict(self):
        self.district.b_setAvailable(1)
        messenger.send('districtOpened')
