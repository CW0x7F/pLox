
from Token import _Token

class VarNotExists(Exception):
    def __init__(self, errorToken: _Token =None):
        self.errorToken= errorToken

class Environment:
    def __init__(self,outerEnv: Environment = None):
        self.env: dict[str, object] = {}
        self.outerEnv = outerEnv

 
    def get(self, name:str):
        '''
            try to find a var from map.
            if currently in block outerEnv is alive to cache global stuffs. env stores locals. to search start from inner, then outer.
            if there it is, return value else return dedicated exception to leter upper funcs to handle
        ''' 

        if name in self.env:
            return self.env[name]
        temp = self.outerEnv
        while temp:
            if name in temp.env:
                return temp.env[name]
            temp = temp.outerEnv
        
        return  VarNotExists() 

    def set(self, name, value):
        '''
        Always set name of current scope
        '''
        self.env[name] = value

    def assign(self, name, value):
        '''
        try to find an existing var, then assign expression value to it. 
        '''
        if name in self.env:
            self.env[name] = value
            return value
        temp = self.outerEnv
        while temp:
            if name in temp.env:
                temp.env[name] = value
                return value
            temp = temp.outerEnv
        
                
        return VarNotExists()
