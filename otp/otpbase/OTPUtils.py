def formatDoId(doId):
    strId = str(doId)
    identifier = chr(65 + int(strId[:2]))
    wordLen = 1

    for i, chunk in enumerate(list(strId[2:])):
        if wordLen % 4 == 0:
            identifier += '-'

        wordLen += 1
        identifier += chr(65 + int(chunk) + (i * 2))

    return identifier
