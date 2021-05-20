import json
import os

class BackupManager:

    def __init__(self, path='backups/', extension='.json'):
        self.path = path
        self.extension = extension

    def getFileName(self, category, info):
        fileName = os.path.join(self.path, category) + '/'

        for i in info:
            fileName += str(i) + '_'

        return fileName[:-1] + self.extension

    def load(self, category, info, default=None):
        fileName = self.getFileName(category, info)

        if not os.path.exists(fileName):
            return default

        with open(fileName, 'r') as f:
            return json.load(f)

    def save(self, category, info, data):
        path = os.path.join(self.path, category)

        if not os.path.exists(path):
            os.makedirs(path)

        fileName = self.getFileName(category, info)

        with open(fileName, 'w') as f:
            json.dump(data, f)