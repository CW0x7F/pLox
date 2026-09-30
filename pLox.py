#We rewrite jLox from https://craftinginterpreters.com/ using python, so I call this tiny replica pLox. Right now this is only my research program

import sys

from constants import DEBUG, currentMode,Mode
from Token import Scanner
import error
from parser import Parser
from interpreter import Interpreter


try:
    import readline
except ImportError:
    pass



def process(codeLine):
    
    #scan 
    scanner = Scanner(codeLine)
    parser = Parser(scanner.tokenizer())
    
    
    if error.hadError: 
        error.showError()
        error.hadError=False
        return
    if DEBUG:
        scanner.show()

    # parse 
    interpreter = Interpreter(parser.parse())
    
    if error.hadError:
        error.showError()
        error.hadError = False
        return 

    if DEBUG:
        print("AST Trees:")
        parser.showAllTrees()

    #interprete 
    res = interpreter.do_interpreter()
    if error.hadError:
        error.showError()
        error.hadError = False
        return 
    if currentMode == Mode.REPL:   
        for each in res:
            print(each)
    


def runPrompt():
    global currentMode
    currentMode = Mode.REPL
    print("pLox ver 0.0.1, written by CW")

    while 1:
        codeLine = input("\n> ")
        if codeLine:
            #pass code to error module
            error.codeStr = codeLine
            #user input something 
            process(codeLine)
            
        
        

def runFile(filePath):
    global currentMode
    currentMode = Mode.SCRIPT
    with open(filePath,'r',encoding='utf-8') as f:
        source = f.read()

    if source:
        error.codeStr = source
        process(source)
    else:
        print(f"Failed to read file: [{filePath}] ")



def main():
    '''
    Entry point for the interpreter 
    '''

    if len(sys.argv) == 1: #REPL Mode
        runPrompt()

    elif len(sys.argv) == 2: #FILE Mode
        runFile(sys.argv[1])

    else:  #shouldnt fall here
        print("Usage:\n\t run pLox to enter REPL Mode\t run pLox <pLox script file> to run scripts from file")
        sys.exit(2)
        


if __name__ == "__main__":
    main()