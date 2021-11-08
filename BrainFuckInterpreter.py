from os import error


memoryInitializer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #27
memory = bytearray(memoryInitializer) 
pointer = 0
errorMsg = ""
warningMsg = ""
output = ""
InfiniteLoopChecker = 10000
parenthesisIndex = 0
f = open("BrainFuckCode.txt","r")
content = f.read()
f.close()

def CheckOutOfBound(point):
    global errorMsg
    if(point < 0 or point > len(memory) - 1):
        errorMsg = "Pointer Out of Bounds"
        return True
    return False

def CheckOutOfRange(val):
    global pointer
    helper = memory[pointer]
    if(val > 0):
        if(helper + val > 255):
            memory[pointer] = 0
        else:
            memory[pointer] += val
    else:
        if(helper + val < 0):
            memory[pointer] = 255
        else:
            memory[pointer] += val

def CheckInput(val):
    global errorMsg
    global warningMsg
    if(len(val) == 0):
        errorMsg = "Input cannot be null"
        return True
    if(len(val) > 1):
        warningMsg = "Symbol: ',' take in consideration only the first character the other will be discarded"
        memory[pointer] = ord(val[0])
        return False
    memory[pointer] = ord(val)
    return False

def FindCorrespective(content, index):
    newIndex = 0
    helper = content[index:]
    doNotRepeat = 0
    for x in helper:
        if(doNotRepeat > newIndex):
            newIndex += 1
            continue
        if(x == "[" and newIndex != 0):
            doNotRepeat = FindCorrespective(helper, newIndex) + 1
        if(x == "]"):
            return newIndex + index
        newIndex += 1

def CheckParenthesis(content):
    global errorMsg
    if(content.count("[") != content.count("]")):
        errorMsg = "Missing Parenthesis!!"
        return False
    return True

def BrainFuckReader(content):
    global InfiniteLoopChecker
    InfiniteLoopChecker -= 1
    fileIndex = 0
    if(InfiniteLoopChecker <= 0):
        return fileIndex
    global pointer
    global output
    global errorMsg
    indexToNotRepeatParenthesis = 0
    for x in content:
        if(errorMsg != ""):
            break
        if(indexToNotRepeatParenthesis > fileIndex):
            fileIndex += 1
            continue
        if(x == "+"):
            CheckOutOfRange(1)
        elif(x == "-"):
            CheckOutOfRange(-1)
        elif (x == ">"):
            pointer += 1
            if(CheckOutOfBound(pointer)):
                break
        elif (x == "<"):
            pointer -= 1
            if(CheckOutOfBound(pointer)):
                break
        elif(x == "."):
            output += chr(memory[pointer]) + " "
        elif(x == ","):
            if(CheckInput(input())):
                break
        elif(x == "["):
            index = FindCorrespective(content, fileIndex)
            if(fileIndex != 0):
                if(memory[pointer] != 0):
                    indexToNotRepeatParenthesis = BrainFuckReader(content[fileIndex:index + 1])
                    indexToNotRepeatParenthesis += fileIndex
                else:
                    return index + 1
        elif(x == "]"):
            if(memory[pointer] == 0):
                return fileIndex + 1
            if(content[0] == "["):
                BrainFuckReader(content)
        else:
            fileIndex += 1
            continue
        fileIndex += 1
    return fileIndex

if(CheckParenthesis(content)):
    BrainFuckReader(content)

if(errorMsg != ""):
    print("Error:", errorMsg)
print()
for x in memory:
    print(x, " ", end="")
print("\npointer pos:", pointer + 1)
print("\nOutput:", output)
if(warningMsg != ""):
    print("Warning:", warningMsg)