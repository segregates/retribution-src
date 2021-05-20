from bisect import bisect_left
import WhiteListData, BlackListData
import re

class WhiteList:

    def __init__(self, sequenceList=[]):
        self.setChatType(0)
        self.setSequenceList(sequenceList)

    def setChatType(self, chatType):
        if chatType == 0:
            self.setWords(WhiteListData.WHITELIST)
        elif chatType == 1:
            self.setWords(BlackListData.BLACKLIST)
        
        self.chatType = chatType

    def setWords(self, words):
        self.words = words
        self.numWords = len(self.words)

    def setSequenceList(self, sequences):
        self.sequenceList = sequences

    def getSequenceList(self, word):
        return self.sequenceList[word] if word and word in self.sequenceList else None

    def cleanText(self, text):
        return text.strip('.,?!').lower()

    def isWord(self, text):
        return self.cleanText(text) in self.words

    def isPrefix(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)

        try:
            word = self.words[i]
        except:
            return False
        
        if self.chatType == 0:
            return word.startswith(text)
        elif self.chatType == 1:
            return word != text

    def getReplacement(self, text, av=None):
        if not av:
            return '\x01red\x01%s\x02' % text
        elif av == base.localAvatar:
            return '\x01italic\x01%s\x02' % text
        else:
            return av.garble(len(text.split(' ')))

    def processText(self, text, av=None):
        if not self.words:
            return text

        words = text.split(' ')
        newWords = []

        for word in words:
            if ((not word) or self.isWord(word)):
                replace = self.chatType == 1
            else:
                replace = self.chatType == 0
            
            if replace:
                newWords.append(self.getReplacement(word, av))
            else:
                newWords.append(word)

        lastWord = words[-1]

        if not av:
            if (not lastWord) or self.isPrefix(lastWord):
                newWords[-1] = lastWord
            else:
                newWords[-1] = self.getReplacement(lastWord, av)

        return ' '.join(newWords)

    def processSequences(self, text, av=None):
        if not self.sequenceList:
            return text

        words = text.split(' ')

        for wordNum in xrange(len(words)):
            word = words[wordNum].lower()
            sequences = self.getSequenceList(word)

            if not sequences:
                continue

            for sequenceNum in xrange(len(sequences)):
                sequence = sequences[sequenceNum].split()
                total = wordNum + len(sequence) + 1

                if total <= len(words) and sequence == [word.lower() for word in words[wordNum + 1:total]]:
                    words[wordNum:total] = self.getReplacement(' '.join(words[wordNum:total]), av).split()

        return ' '.join(words)

    def processThroughAll(self, text, av=None):
        if (text.startswith('~') and not av):
            return text

        return self.processSequences(self.processText(re.sub(' +', ' ', text), av), av)
