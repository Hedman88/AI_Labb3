from enum import Enum
import fsm, pathfinder

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

class Agent:
    holding = ItemEnum.NONE
    type = AgentType.WORKER
    path = []
    state = fsm.IdleState()
    goal = "wood"
    def __init__(self, ID, spawnPos):
        self.ID = ID
        self.posX = spawnPos[0] * 10 + 5
        self.posY = spawnPos[1] * 10 + 5

    def Update(self):
        self.state.Execute(self)

    def Upgrade(self, newType):
        if(newType == AgentType.DISCOVERER):
            # 60 second timer
            self.type = newType
        elif(newType == AgentType.SOLDIER):
            # Check for weapon
            # 60 second timer
            self.type = newType
        else:
            # 120 second timer
            self.type = newType

    def ChangeState(self, newState):
        self.state = newState

    def Move(self, ms, dirX, dirY):
        self.posX = self.posX + ms*dirX
        self.posY = self.posY + ms*dirY

    def PickUpItem(self):
        if(self.type != AgentType.WORKER):
            print(self.ID, "is not a worker")
            return
        if(self.holding != ItemEnum.NONE):
            print(self.ID, "is already carrying", self.holding)
            return
        else:
            self.holding = ItemEnum.WOOD

    def FindWood(self):
        self.path = pathfinder.pf.bfs(self.GetTouchingBlock())

    def GetTouchingBlock(self):
        blockID = int(self.posY / 10) * 100 + (int(self.posX / 10))
        return pathfinder.paths.GetBlockByID(blockID)