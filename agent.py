import fsm, pathfinder, enums

class Agent:

    def __init__(self, ID, spawnPos):
        self.ID = ID
        self.posX = spawnPos[0] * 10 + 5
        self.posY = spawnPos[1] * 10 + 5
        self.hubBlock = self.GetTouchingBlock()

        self.holding = enums.ItemEnum.NONE
        self.type = enums.AgentType.WORKER
        self.path = []
        self.pathBack = []
        self.state = fsm.IdleState()
        self.goal = enums.GoalEnum.WOOD_GOAL
        self.woodChopTimer = 30
        self.UpgradeTimer = 0

    def Update(self):
        self.state.Execute(self)

    def SetHubBlock(self, hubBlock):
        self.hubBlock = hubBlock

    def Upgrade(self, newType):
        if(newType == enums.AgentType.DISCOVERER):
            self.UpgradeTimer = 60
            self.type = newType
        elif(newType == enums.AgentType.SOLDIER):
            # Check for weapon
            # 60 second timer
            self.type = newType
        else:
            # Alla hantverkare här
            self.UpgradeTimer = 120
            self.type = newType

    def SetType(self, newType):
        self.type = newType

    def ChangeState(self, newState):
        self.state = newState

    def Move(self, ms, dirX, dirY):
        self.posX = self.posX + ms*dirX
        self.posY = self.posY + ms*dirY

    def PickUpItem(self):
        if(self.type != enums.AgentType.WORKER):
            print(self.ID, "is not a worker")
            return
        if(self.holding != enums.ItemEnum.NONE):
            print(self.ID, "is already carrying", self.holding)
            return
        else:
            self.holding = enums.ItemEnum.WOOD

    def DropItem(self):
        if (self.type != enums.AgentType.WORKER):
            print(self.ID, "is not a worker")
            return
        if (self.holding == enums.ItemEnum.NONE):
            print(self.ID, "has nothing on them to drop")
            return
        else:
            self.GetTouchingBlock().DropWood()
            self.holding = enums.ItemEnum.NONE

    def FindWood(self):
        self.pathBack = []
        self.path = []
        pathfinder.pf.Reset()
        self.path = pathfinder.pf.bfs(self.GetTouchingBlock())

    def SetReturnPath(self):
        # self.path = pathfinder.pf.AStar(self.GetTouchingBlock(), self.hubBlock)
        self.path = self.pathBack
        self.pathBack = []
        print("return path set")

    def GetTouchingBlock(self):
        blockID = int(self.posY / 10) * 100 + (int(self.posX / 10))
        return pathfinder.paths.GetBlockByID(blockID)