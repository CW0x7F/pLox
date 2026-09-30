from enum import Enum,auto

#toggle debug mode
DEBUG = True


#mark the Modes of current program
class Mode(Enum):
    REPL = auto()
    SCRIPT = auto()

currentMode = None
    