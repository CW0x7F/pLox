from enum import Enum, auto

class TokenType(Enum):

    #keywords
    RET = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    VAR = auto()
    NIL = auto()
    FOR = auto()
    TRUE = auto()
    FALSE= auto()
    CLASS = auto()
    AND = auto()
    OR = auto() 
    FUN = auto()
    PRINT  = auto()
    SUPER = auto()
    THIS = auto()


    #operators 
    EQUAL = auto()
    #NOT_EQUAL = auto()
    EQUAL_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR  = auto()
    SLASH = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    

    #PUNCTUATIONS 
    SEMICOLON = auto()
    COMMA = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    DOT = auto()
    EOF = auto()

    #LITERALS 
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

