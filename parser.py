from Expr import *
from TokenType import TokenType
from Token import  _Token
from error import setError


class Parser:
    def __init__(self, tokens:list[_Token]):
        self.tokens = tokens
        self.trees: list[Expr] = [] 
        self.cur = 0 #index in token list


    def _sync(self):
        '''
        function use to align to next stmt, if there is malfomred tokens 
        advance to next token after ; or look for a keyword which starts a 
        stmt
        '''
        while not self._isAtEnd():
            if self.tokens[self.cur].type == TokenType.SEMICOLON:
                return
            self.cur+=1

    def parse(self):

        self._program()
        return self.trees

    def _program(self):
        while not self._isAtEnd():
            try:
                self.trees.append(self._declaration())
            except parseError as e:
                self._sync()
                setError(e.pos,e.line,e.errMsg)

    
    def _declaration(self):
        if self._match(TokenType.VAR):
            return self._varDecl()
        return self._statement()


    def _varDecl(self):
        token = self.tokens[self.cur]
        if self._match(TokenType.IDENTIFIER):
            name = token.value
            expr = None
            while self._match(TokenType.EQUAL):
                expr = self._expression()

            self._terminateLine()

            return VarDecl(name,expr)

        else:
            ctoken = self.tokens[self.cur]
            raise parseError("Expect assignment sign '='",ctoken.pos, ctoken.line,)


    def _terminateLine(self):
        if self._match(TokenType.SEMICOLON) or self._isAtEnd():
            return
        etoken = self.tokens[self.cur]
        raise parseError("Expect ';' to terminate the statement",etoken.pos,etoken.line)


    def _statement(self):
        if self._match(TokenType.PRINT):
            return printStmt(self._printStmt())
        if self._match(TokenType.LEFT_BRACE):
            return self._blockStmt()
                
        return exprStmt(self._exprStmt())


    def _blockStmt(self):
        innerStmts = []
        while not self._isAtEnd() and not self.tokens[self.cur].type == TokenType.RIGHT_BRACE:
            innerStmts.append(self._declaration())

        ctoken = self.tokens[self.cur]
        if ctoken.type != TokenType.RIGHT_BRACE:
            raise parseError("Expect right brace '}'", ctoken.pos, ctoken.line)
        self.cur+=1
        return BlockStmt(innerStmts)

    def _printStmt(self):
        return self._exprStmt()

    def _exprStmt(self):
        expr = self._expression()
        self._terminateLine()
        return expr


    def _expression(self):
        return self._assignment()

    def _assignment(self):
        cacheToken = self.tokens[self.cur]
        expr = self._equality()
        if self._match(TokenType.EQUAL):
            #assignment branch
            if not isinstance(expr, Var):
                raise parseError("Left value must be a identifier",cacheToken.pos,cacheToken.line )
            rvalue = self._assignment()
            return Assign(expr, rvalue)
        return expr
            
   
    def _equality(self) ->Expr:
        return self._binary(
            self._comparison,
            TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL
        )

   
    def _comparison(self)->Expr:
        return self._binary(
            self._term,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL
        )

    
    def _term(self):
        return self._binary(
            self._factor,
            TokenType.MINUS,TokenType.PLUS
        )   

    
    def _factor(self):
        return self._binary(
            self._unary,
            TokenType.SLASH, TokenType.STAR
        )

   
    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self.tokens[self.cur-1]
            right = self._unary()
            return Unary(operator,right)
        return self._primary()

   
    def _primary(self):
        
        type = self.tokens[self.cur].type
        self.cur+=1
        match type:
            case TokenType.NUMBER | TokenType.STRING:
                return Literal(self.tokens[self.cur-1].value)
            case TokenType.TRUE:
                return Literal(True)
            case TokenType.FALSE:
                return Literal(False)
            case TokenType.NIL:
                return Literal(None)
            case TokenType.IDENTIFIER:
                return Var(self.tokens[self.cur-1])
            case TokenType.LEFT_PAREN:
                expr = self._expression()
                '''
                if DEBUG:
                    print(expr, self.tokens[self.cur].type, self.tokens[self.cur].pos, self.tokens[self.cur].type,)
                '''
                if self.tokens[self.cur].type == TokenType.RIGHT_PAREN: 
                    self.cur+=1
                    return Grouping(expr)
                raise parseError("Expect right paren!",self.tokens[self.cur].pos,self.tokens[self.cur].line)
            case _:
                raise parseError("Expect expression!",self.tokens[self.cur-1].pos,self.tokens[self.cur-1].line)
           
                        

    def _binary(self, oprand, *ops):
        left = oprand()
        while self._match(*ops):
            operator = self.tokens[self.cur-1]
            right = oprand()
            left = Binary(left,operator,right)
        return left

    def _match(self, *ops: TokenType)->bool:
        for each in ops:
            if each == self.tokens[self.cur].type:
                self._consume()
                return True

        return False


    def _consume(self):
        token = self.tokens[self.cur]
        self.cur+=1
        return token
    

    def _isAtLineEnd(self):
        return self.tokens[self.cur].type == TokenType.SEMICOLON or self._isAtEnd()

    def _isAtEnd(self):
        return self.tokens[self.cur].type == TokenType.EOF

    def _peek(self):
        if self.cur >= len(self.tokens):
            #there is always an eof, should never go here
            return TokenType.EOF
        return self.tokens[self.cur+1]

    def showAllTrees(self):
        for each in self.trees:
            self._show(each)
            print("") #\n


    def _show(self,node):
            if isinstance(node,Binary):
                print(f"( {node.operator.type.name}",end="")
                self._show(node.left)
                self._show(node.right)
                print(" )",end="")
            elif isinstance(node,Literal):
                print(f" {node.value}",end="")
            elif isinstance(node,Unary):
                print(f"( {node.operator.type.name}",end="")
                self._show(node.right)
                print(" )",end="")
            elif isinstance(node, Grouping):
                print("( ",end="")
                self._show(node.expr)
                print(" )",end="")
            #elif isinstance(node, )


class parseError(Exception):
    def __init__(self, errMsg, pos, line):
        super().__init__(errMsg)
        self.errMsg = errMsg
        self.pos = pos
        self.line = line 