from TokenType import TokenType
from constants import DEBUG
from error import setError
import operator

class _Token:

    def __init__(self, type, value, line,pos):
        self.type = type
        self.value = value
        self.line = line
        self.pos = pos


class Scanner:

    def __init__(self, source):
        self.codeline = source
        self.curLine =1
        self.cur = 0
        self.tokenList: list[_Token] = []


    def tokenizer(self):
        '''
        receive a code str either from REPL or from a script file, then output a serious of tokens, end with EOF token
        '''
        
        while not self._isAtEnd():
            c = self._consume()
            match c:
                case '('|')'|'{'|'}'|'+'|'-'|'*'|','|'.'|';':
                    self._add_token(self.TOKEN_MAP[c][0],self.cur-1,self.TOKEN_MAP[c][1])
                case '!' | '<' | '>' | '=':
                    if self._peek() == '=':
                        self.cur+=1              
                        self._add_token(self.TOKEN_MAP[c+'='][0],self.cur-2,self.TOKEN_MAP[c+'='][1])
                    else: 
                        self._add_token(self.TOKEN_MAP[c][0],self.cur-1,self.TOKEN_MAP[c][1])

                case '/':
                    if self._peek() == '/':
                        #in comment
                        self.cur+=1
                        self.curLine+=1
                        while not self._isAtEnd() and self._consume()!='\n':
                            pass
                    else:
                        #simply slash
                        self._add_token(TokenType.SLASH,self.cur-1,self.TOKEN_MAP[c][1])
                        
                case '"':
                    strLiteral = "" 
                    pos = self.cur
                    while not self._isAtEnd() and self._peek() != '"':
                        strLiteral+= self._consume()
                    self.cur+=1
                    self._add_token(TokenType.STRING,pos,strLiteral)

                case '\n':
                    self.curLine+=1
                
                case _:
                    tokenLen =1
                    if str(c).isspace():
                        pass
            
                    elif str(c).isdigit():
                        
                        while not self._isAtEnd() and str(self._peek()).isdigit():
                            self._consume() 
                            tokenLen+=1 
                        num = float(self.codeline[self.cur-tokenLen:self.cur])
                        self._add_token(TokenType.NUMBER,self.cur-tokenLen,num)

                    elif str(c).isalpha() or c == '_':
                        while not self._isAtEnd() and (str(self._peek()).isalnum() or self._peek() == '_'):
                            self._consume()
                            tokenLen+=1
                        word = self.codeline[self.cur-tokenLen:self.cur]
                        if word in self.KEYWORDS_MAP:
                            self._add_token(self.KEYWORDS_MAP[word],self.cur-tokenLen)
                        else:
                            self._add_token(TokenType.IDENTIFIER,self.cur-tokenLen,word)

                    else:
                        #it should never falls here, sending unknown token alarm
                        '''
                        #calculate offset in line
                        if self.curLine ==1:
                            lineOffset = self.cur
                            backIndex = 0
                        else:
                            backIndex =self.cur
                            while self.codeline[backIndex] !='\n':
                                backIndex-=1
                            backIndex+=1
                            lineOffset = self.cur - backIndex

                        #culculate line end index
                        while not self._isAtEnd() and self.codeline[self.cur] !='\n':
                            self.cur+=1  #since this line is not going to use any more, we just skip it.
                        '''
                        setError(self.cur-1,self.curLine,"Wrong Token!")

        #attach eof to the end 
        self._add_token(TokenType.EOF,self.cur-1)
        return self.tokenList

                        
                        
    def show(self):
        '''
        this function only used in debug mode to display cooked tokens
        '''
        lineNum = self.tokenList[0].line                    
        for each in self.tokenList:
            if each.line != lineNum:
                print('\n')
                lineNum = each.line

            s=f"({TokenType(each.type).name}"
            if each.value:
                s+=f" {each.value}"
            s+=") "
            print(s,end="")

        print("")
    

    
                    

    def _add_token(self, type, pos, value=None):
        token = _Token(type, value,self.curLine,pos)
        self.tokenList.append(token)
    
    def _peek(self):
        
        return self.codeline[self.cur]

    def _consume(self):
        self.cur+=1
        return self.codeline[self.cur-1]


    def _isAtEnd(self):
        return self.cur >= len(self.codeline)


 

    TOKEN_MAP = {
        '(':[TokenType.LEFT_PAREN,None],
        ')':[TokenType.RIGHT_PAREN,None],
        '{':[TokenType.LEFT_BRACE,None],
        '}':[TokenType.RIGHT_BRACE,None],
        ',':[TokenType.COMMA,None],
        '.':[TokenType.DOT,None],
        '-':[TokenType.MINUS, operator.sub],
        '+':[TokenType.PLUS, operator.add],
        ';':[TokenType.SEMICOLON,None],
        '/':[TokenType.SLASH, operator.truediv],
        '*':[TokenType.STAR, operator.mul],
        '!':[TokenType.BANG, operator.not_],
        "!=":[TokenType.BANG_EQUAL,operator.ne],
        '=':[TokenType.EQUAL,None],
        "==":[TokenType.EQUAL_EQUAL,operator.eq],
        '>':[TokenType.GREATER,operator.gt],
        ">=":[TokenType.GREATER_EQUAL,operator.ge],
        '<':[TokenType.LESS,operator.lt],    
        "<=":[TokenType.LESS_EQUAL,operator.le]
    }

    KEYWORDS_MAP = {
        'and':TokenType.AND,
        'class':TokenType.CLASS,
        'else':TokenType.ELSE,
        'false':TokenType.FALSE,
        'fun': TokenType.FUN,
        'for': TokenType.FOR,
        'if':TokenType.IF,
        'nil':TokenType.NIL,
        'or': TokenType.OR,
        'print':TokenType.PRINT,
        'return': TokenType.RET,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE
    }
    

    
