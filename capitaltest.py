text0 = "está floja. ¡aprétala!"
text1 = "¡Jala a este! no quiere meterse en el agua"
text2 = "¿No quieres que me acueste? me voy a descansar aquí, dijo"
text3 = "¿No quieres que me acueste? ¿me voy a descansar aquí? dijo"
text4 = "¡Cubre a tu hijo! ¡qué lo tapes con su cobija!"
text5 ="“hay muchos hongos. ¿no les dije que hay muchos? ¿por qué no me siguieron?” le dijo"
textList = [text0,text1,text2,text3,text4,text5]


def secondSentence(line, chr):
    '''this might have to be modified eventually for multiple second sentence'''
    quotes = r'’”"'
    n = line.index(chr)
    if line[n+1] in quotes:
        newline = line
    else:
        newline = line[:n+2] + line[n+2].upper() + line[n+3:]
    return newline

def capString(line, n):
    if n == 0:
         secondPass = line[:n+1] + line[n+1].upper() + line[n+2:]
    elif line[n-2] == ',':
        secondPass = line
    else:
        secondPass = line[:n+1] + line[n+1].upper() + line[n+2:]
    return secondPass

def fixCapitalization(text):
    '''add capital letters'''
    quotes = r'“‘"'
    if text[0] in quotes:
        firstPass = text[0] + text[1].upper() + text[2:]
    else:
        firstPass = text[0].upper() + text[1:]
    '''hack to capitalize after Spanish initial punctuation'''
    if '¿' in firstPass:
        indexlist = [i for i, ltr in enumerate(firstPass) if ltr == '¿']
        secondPass = firstPass
        for index in indexlist:
            secondPass = capString(secondPass,index)
        if secondPass.index('?') != len(secondPass) - 1:
            secondPass = secondSentence(secondPass,'?')
            print(secondPass)
    else:
        secondPass = firstPass
    if '¡' in secondPass:
        indexlist = [i for i, ltr in enumerate(secondPass) if ltr == '¡']
        newtext = secondPass
        for index in indexlist:
            newtext = capString(newtext,index)
        if newtext.index('!') != len(newtext) - 1:
            newtext = secondSentence(newtext,'!')
            print(newtext)
    else:
        newtext = secondPass
    return newtext


for line in textList:
    print(fixCapitalization(line))

