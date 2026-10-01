from Expr import *
from Token import _Token
from TokenType import TokenType
from Environment import *
from error import setError,setPlainError
import operator

class Interpreter:

    env = Environment()

    def __init__(self,trees):
        self.trees = trees
        self.results = []

    def do_interpreter(self):
        '''
        interface func in Interpreter. process given trees, and then output a result.
        '''
        try: 
            for eachtree in self.trees:
                res = self._checkDecl(eachtree)
                if not isinstance(res,NoReturnValue):
                    self.results.append(res)
            return self.results
        except VarNotExists as e:
            setError(e.errorToken.pos,e.errorToken.line,"This variable doesn't exist!")

        except LoxRuntimeError as e:
            setError(e.errToken.pos, e.errToken.line, e.msg)
        except InternalError as e:
            setPlainError(e.msg)

    def _checkDecl(self, node):
        '''
        declaration -> varDecl | statement
        '''
        match node: 
            case VarDecl():
                self._checkVarDecl(node)
                return NoReturnValue()
            case Stmt():
                return self._checkStmt(node)
            case _:
                raise InternalError(f"Not a statement: {type(node).__name__}")


    def _checkVarDecl(self, node):
        '''
        For varDecl, Lox allows redefination to make it easier to use in REPL mode. Also to keep consistency this is also supported in script mode.
        '''
        self.env.set(node.name, self._evaluate(node.initializer))


    def _checkStmt(self, node):
        '''
        statement -> exprStmt | printStmt | blockStmt | ifStmt | whileStmt
       
        '''
        match node:
            case exprStmt(expr = expr):
                return self._evaluate(expr)

            case printStmt(expr=expr):
                print(self._evaluate(expr))
                return NoReturnValue()

            case BlockStmt():
                self._checkBlock(node)
                return NoReturnValue()

            case IfStmt():
                self._checkIf(node)
                return NoReturnValue()

            case whileStmt():
                self._checkWhile(node)
                return NoReturnValue()
            case _:
                raise InternalError(f"Unknown statement: {type(node).__name__}")
           
                

    
    def _checkWhile(self, node:whileStmt):
        while self._evaluate(node.test):
            self._checkStmt(node.body)

    def _checkIf(self, node:IfStmt):
        if self._evaluate(node.test):
            self._checkStmt(node.then)
        elif node.elseBlock:
            self._checkStmt(node.elseBlock)


    def _checkBlock(self, node:BlockStmt):
        '''
         For block, we neeed a dedicated local scope to store vars.
        '''
        localenv= Environment(self.env)
        oldenv = self.env
        self.env = localenv
        
        for each in node.statements:
            self._checkDecl(each)

        #after that we switch it back 
        self.env = oldenv

  


    def _evaluate(self, node):
        '''
        core func for exprs in Interpreter
        receives a expr tree node, then recursively generate and return result of this tree
        '''    
        match node:
            case Binary(left=left, op=op, right=right):
                if op.value:
                    lvalue = self._evaluate(left)
                    rvalue = self._evaluate(right)
                    kind = type(lvalue)

                    if op.value not in (operator.eq, operator.ne) and kind != type(rvalue):
                        raise LoxRuntimeError(op,"Mismatch left and right types!")  
                    match op.value:
                        case operator.add:
                            if kind not in (float,str): 
                                raise LoxRuntimeError(op,"Unsupported left or right type for add operator!")
                        case operator.sub | operator.mul | operator.truediv:
                            if kind is not float:
                                raise LoxRuntimeError(op,"Oprands must be numbers for this operator!")
                    return op.value(lvalue,rvalue)
            case Unary(operator=op, right=right):
                if op.type == TokenType.BANG:
                    return not self._evaluate(right)
                if op.type == TokenType.MINUS:
                    rvalue = self._evaluate(right)
                    if type(rvalue) != float:
                        raise LoxRuntimeError(op,"Oprand must be number for this operator!")   
                    return (-rvalue)
            case Grouping(expr= expr):
                return self._evaluate(expr)
            case Literal(value=value):
                return value
            case Var(token=token):
                res =  self.env.get(token.value)
                if isinstance(res,VarNotExists):
                    raise VarNotExists(token)
                return res
                    
            case Assign(identifier=identifier, value= value):
                
                res = self.env.assign(identifier.token.value,self._evaluate(value))
                if isinstance(res,VarNotExists):
                    raise VarNotExists(identifier.token)
                return res 

            case LogicOR(left=left, right=right):
                return self._evaluate(left) or self._evaluate(right)

            case LogicAND(left=left, right=right):
                return self._evaluate(left) and self._evaluate(right)
                
    
class LoxRuntimeError(Exception):
    def __init__(self, errToken, msg):
        self.errToken = errToken
        self.msg = msg

class NoReturnValue:
    pass

class InternalError(Exception):
    def __init__(self, msg):
        self.msg = msg