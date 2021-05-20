from otp.otpbase import OTPLocalizer
import random

class ChatGarbler:

    def getMessages(self):
        return OTPLocalizer.ChatGarblerDefault

    def garble(self, numWords):
        wordList = self.getMessages()
        return '\x01italic\x01%s\x02' % ' '.join([random.choice(wordList) for i in xrange(numWords)])
