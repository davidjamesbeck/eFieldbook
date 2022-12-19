indexList = ['tu:\ttu:\tEX1234:1', 'tu:\ttu:\tEX1234:2', 'tu:\ttu:\tEX1235:2', 'chi\tchi\tEX1234:4']
prevMorph = ''
trimmedList = []
for i, item in enumerate(indexList):
    print(item)
    index = item.index('\tEX')
    if item[:index-1] != prevMorph:
        prevMorph = item[:index-1]
        trimmedList.append(item)
    else:
        trimmedList[-1] += item[index:]
print(trimmedList)
