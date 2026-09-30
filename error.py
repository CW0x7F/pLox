#error related
hadError = False
position: list[int] = []
errorMsg: list[str] = []
errorline: list[int] = []
codeStr = ""

def setError(pos, line, msg):
    global codeStr,hadError,position,errorMsg, errorline
    position.append(pos) 
    errorMsg.append(msg)
    hadError = True
    errorline.append(line)
    

def showError():

    i=0
    while i< len(position):
        s = f"Line [{errorline[i]}]:  "
        targetLine,inLineOffset = _findCodeStr(i)
        print(_red(f"{errorMsg[i]}\n{s}{targetLine}\n"+" "*(inLineOffset+len(s)-1)+"^"))
        i+=1

    _clearBuf()
    
def _findCodeStr(i):
    #using pos go back and forth to target the whole line
    head = position[i]
    while head>=0 and codeStr[head] != '\n':
        head-=1
    tail = position[i]
    while tail<len(codeStr) and codeStr[tail] !='\n':
        tail+=1

    return codeStr[head+1:tail],position[i]-head
    

def _clearBuf():
    global position,errorMsg,errorline,codeStr
    position = []
    errorline = []
    errorMsg = []
    codeStr = ""

def _red(text):
    return f"\033[31m{text}\033[0m"
