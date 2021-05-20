from panda3d.core import Filename, Light, NodePath, Texture
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase.Loader import Loader
import PiratesGlobals
import os

class PiratesLoader(Loader):

    def __init__(self, base):
        Loader.__init__(self, base)
        self.textureCache = {}
        self.fontCache = {}
        self.soundCache = {}
        self.modelCache = {}

    def destroy(self):
        del self.textureCache
        del self.fontCache
        del self.soundCache
        del self.modelCache
        Loader.destroy(self)

    def preloadModels(self):
        for model in PiratesGlobals.preLoadSet:
            self.loadModel(model)

    def scanDirectory(self, directory, extensions=[]):
        fileNames = []

        def recursive(directory):
            files = vfs.scanDirectory(directory)
            
            if not files:
                return

            for file in files:
                if file.isDirectory():
                    recursive(file.getFilename())
                else:
                    fileName = file.getFilename().getFullpath()[1:]
                    extension = os.path.splitext(fileName)[1][1:]

                    if extension in extensions:
                        fileNames.append(fileName)

        recursive('/' + directory)
        return fileNames

    def preloadModelsFrom(self, directory):
        for file in self.scanDirectory(directory, ['bam', 'egg']):
            loader.loadModel(file)

    def loadModel(self, *args, **kw):
        modelName = args[0].replace('.bam', '').replace('\\', '/').split('/')[-1]
        
        if 'customOptions' in kw:
            customOptions = kw['customOptions']
            del kw['customOptions']
        else:
            customOptions = {}
        
        if modelName in self.modelCache:
            model = self.modelCache[modelName]
        else:
            kw['noCache'] = True

            model = Loader.loadModel(self, *args, **kw)
            
            if not model:
                return

            flattenType = customOptions.get('flattenType')
            
            if flattenType:
                if flattenType == 'light':
                    model.flattenLight()
                elif flattenType == 'medium':
                    model.flattenMedium()
                elif flattenType == 'strong':
                    model.flattenStrong()                    
            
            transformFunc = customOptions.get('transformFunc')
            
            if transformFunc:
                model = transformFunc(model)
            
            model = model.node()
            self.modelCache[modelName] = model

        return NodePath(model.copySubgraph())

    def loadFont(self, *args, **kw):
        fontId = (args[0], frozenset(kw.items()))
        
        if fontId not in self.fontCache:
            font = Loader.loadFont(self, *args, **kw)
            self.fontCache[fontId] = font
            return font
        else:
            return self.fontCache[fontId]

    def loadTexture(self, texturePath, alphaPath = None, okMissing = False):
        textureId = (texturePath, alphaPath)
        
        if textureId not in self.textureCache:
            texture = Loader.loadTexture(self, texturePath, alphaPath, okMissing=okMissing)
            self.textureCache[textureId] = texture
            return texture
        else:
            return self.textureCache[textureId]

    def loadMusic(self, soundPath):
        if soundPath not in self.soundCache:
            sound = Loader.loadMusic(self, soundPath)
            self.soundCache[soundPath] = sound
            return sound
        else:
            return self.soundCache[soundPath]
