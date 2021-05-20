from pirates.piratesbase import PiratesGlobals
import copy
import random

class CLerpSeaPatchInterval():
    def __init__(self, name, duration, blendType, patch, initial, target):
        self.name = 'Default Name'
        self.duration = 1.2
        self.blendType = blendType
        self.patch = patch
        self.initial = initial
        self.target = target

    def lerpNum(self):
        self.lerpNum = 0.1
