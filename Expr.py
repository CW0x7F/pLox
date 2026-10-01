from Token import _Token

class Expr:
   pass

class Binary(Expr):
   def __init__(self, left, op:_Token, right,):
      self.left = left
      self.op = op
      self.right = right


class Literal(Expr):
   def __init__(self, value,):
      self.value = value


class Unary(Expr):
   def __init__(self, operator:_Token, right,):
      self.operator = operator
      self.right = right


class Grouping(Expr):
   def __init__(self, expr,):
      self.expr = expr

class Var(Expr):
   def __init__(self, token):
      self.token = token 


class Assign(Expr):
   def __init__(self, identifier:Var, value:Expr):
      self.identifier = identifier
      self.value = value

class LogicOR(Expr):
   def __init__(self, left, right):
      self.left = left
      self.right = right

class LogicAND(Expr):
   def __init__(self, left, right):
      self.left = left
      self.right = right 



class Stmt:
   pass

class exprStmt(Stmt):
   def __init__(self,expr):
      self.expr = expr

class printStmt(Stmt):
   def __init__(self,expr):
      self.expr = expr

class BlockStmt(Stmt):
   def __init__(self, statements):
      self.statements = statements

class VarDecl(Expr):
   def __init__(self, name, initializer):
      self.name = name
      self.initializer = initializer

class IfStmt(Stmt):
   def __init__(self, test, then, elseBlock):
      self.test = test
      self.then = then
      self.elseBlock = elseBlock

class whileStmt(Stmt):
   def __init__(self, test, body):
      self.test = test
      self.body = body



