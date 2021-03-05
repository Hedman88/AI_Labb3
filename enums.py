from enum import Enum

class ItemEnum(Enum):
    NONE = 0
    WOOD = 1
    IRON_ORE = 2
    IRON_INGOT = 3

class AgentType(Enum):
    WORKER = 0
    DISCOVERER = 1
    SOLDIER = 2
    KILNER = 3
    SMITH = 4
    SMELTER = 5
    BUILDER = 6

class GoalEnum(Enum):
    WOOD_GOAL = 0
    #F
