import re

'''
script for extracting speaker and time codes from glosses
'''

def getTime(gloss):
    '''
    extracts a time code of format "[H:MM(:SS)(.NNNNNN))]" 
    and returns it along with the gloss minus time
    '''
    regex = '\[(\d*)(:\d\d)(:\d\d){0,1}(.\d*){0,}\]'
    m = re.search(regex,gloss)
    if m != None:
        timeCode = m.group(0)[1:-1]
        gloss = gloss[:m.start()].strip()
        rangeEx = '-|–'
        k = re.search(rangeEx, timeCode)
        if k != None:
            if '-' in timeCode:
                codes = timeCode.split('-')
            else:
                codes = timeCode.split('–')
            timeCode = codes[0].strip()
            endTime = codes[1].strip()
        else:
            endTime = None
    else:
        timeCode = None
        endTime = None
    return timeCode, endTime, gloss

def getSpokenBy(gloss):
    checkGloss = gloss.split(' ')
    if checkGloss[0][-1] == ":":
        pieces = gloss.partition(':')
        spokenBy = pieces[0]
        gloss = pieces[2]
    else:
        spokenBy = None
    return spokenBy, gloss
