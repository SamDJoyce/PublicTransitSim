from enum import Enum, auto


class State(Enum):
    INIT = auto()
    IDLE = auto()
    HEADING_TO_ROUTE_START = auto()
    AT_STOP = auto()
    DWELL = auto()
    IN_TRANSIT = auto()
    BREAKDOWN = auto()
    DELAYED = auto()
    ROUTE_COMPLETE = auto()
    OUT_OF_SERVICE = auto()


