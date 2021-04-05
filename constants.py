from enum import Enum, auto

class cx_status(Enum):
    CONNECTED = auto()
    ERROR = auto()
    NOT_LISTENING = auto()
