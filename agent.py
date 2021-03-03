from enum import Enum
import fsm

class ItemEnum(Enum):
    NONE = 0
    WOOD = 1
    IRON_ORE = 2
    IRON_INGOT = 3

class Agent:
    holding = ItemEnum.NONE
    state = fsm.IdleState()
    def __init__(self, ID):
        self.ID = ID
        self.CheckNeeds()


