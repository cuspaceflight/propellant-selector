from enum import Enum

# TC: "This is worth having. How could you possibly be ok with completely
# unreadable conditionals on random constants???"

class Phase(Enum):
    """Does what it says on the tin"""
    LIQUID    = 0
    GAS       = 1
    TWO_PHASE = 2

