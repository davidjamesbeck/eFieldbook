"""generates unique id numbers for various types of elements"""


def generateID(prefix, dictionary):
    codeList = sorted(dictionary.keys(), key=lambda i : int(i[2:]))
    if len(codeList) != 0:
        topCode = int(codeList[-1][2:])
        topCode += 1
    else:
        topCode = 1
    newID = prefix + str(topCode)
    while newID in codeList:
        topCode += 1
        newID = prefix + str(topCode)
    return newID
