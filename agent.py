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
        self.workTimer = 30
        self.upgradeTimer = 0
        self.workPlace = 0

    def Update(self):
        self.state.Execute(self)

    def SetGoal(self, newGoal):
        self.goal = newGoal

    def SetHubBlock(self, hubBlock):
        self.hubBlock = hubBlock

    def AddWorkPlace(self, workPlace):
        if self.workPlace == 0:
            self.workPlace = workPlace
        else:
            print(self.ID, "already has a workplace at", self.workPlace)

    def Upgrade(self, newType):
        if(newType == enums.AgentType.DISCOVERER):
            self.upgradeTimer = 60
            self.ChangeState(fsm.UpgradeState(enums.AgentType.DISCOVERER))
        elif(newType == enums.AgentType.SOLDIER):
            # Check for weapon
            self.upgradeTimer = 60
            # self.ChangeState(fsm.UpgradeState())
        elif(newType == enums.AgentType.KILNER):
            # Alla hantverkare här
            self.upgradeTimer = 120
            self.ChangeState(fsm.UpgradeState(enums.AgentType.KILNER))
        elif(newType == enums.AgentType.BUILDER):
            self.upgradeTimer = 120
            self.ChangeState(fsm.UpgradeState(enums.AgentType.BUILDER))

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

    def FindTask(self):
        if self.type == enums.AgentType.WORKER:
            if self.goal == enums.GoalEnum.WOOD_GOAL:
                self.FindWood()
                return
        if self.goal == enums.GoalEnum.DISCOVER_GOAL:
            if self.type != enums.AgentType.DISCOVERER:
                self.Upgrade(enums.AgentType.DISCOVERER)
                return
            else:
                self.ChangeState(fsm.ExploreState())
                return

        if self.goal == enums.GoalEnum.KILN_GOAL:
            if self.type != enums.AgentType.KILNER:
                self.Upgrade(enums.AgentType.KILNER)
                return
            elif self.workPlace != 0:
                b = self.GetTouchingBlock()
                if b is not self.workPlace.block:
                    self.SetReturnPath()
                    return
                else:
                    self.ChangeState(fsm.RunKilnState())
                    return
            else:
                #print("looking for workplace")
                return

        if self.goal == enums.GoalEnum.BUILD_KILNS_GOAL:
            if self.type != enums.AgentType.BUILDER:
                self.Upgrade(enums.AgentType.BUILDER)
                return
            else:
                b = self.GetTouchingBlock()
                if b is not self.hubBlock:
                    self.SetReturnPath()
                    return
                if b.woodPile >= 10 and len(b.kilns) < 4:
                    self.Build(enums.BuildingType.KILN_BUILDING)
                else:
                    self.ChangeState(fsm.IdleState())

    def FindWood(self):
        self.pathBack = []
        self.path = []
        pathfinder.pf.Reset()
        self.path = pathfinder.pf.bfs(self.GetTouchingBlock())
        if self.path == None:
            #print("No trees in sight")
            return
        self.ChangeState(fsm.MoveState())

    def DiscoverTiles(self):
        if self.type != enums.AgentType.DISCOVERER:
            print("This unit is not a discoverer!!!")
            return
        b = self.GetTouchingBlock()
        for nID in b.adjacents:
            pathfinder.paths.GetBlockByID(nID).Discover()
        bNeighbours = []
        bCoords = b.IdToCoordinates()
        bNeighbours.append((bCoords[1] - 1) * 100 + bCoords[0])         #N
        bNeighbours.append((bCoords[1] - 1) * 100 + bCoords[0] + 1)     #NE
        bNeighbours.append(bCoords[1] * 100 + bCoords[0] + 1)           #E
        bNeighbours.append((bCoords[1] + 1) * 100 + bCoords[0] + 1)     #SE
        bNeighbours.append((bCoords[1] + 1) * 100 + bCoords[0])         #S
        bNeighbours.append((bCoords[1] + 1) * 100 + bCoords[0] - 1)     #SW
        bNeighbours.append(bCoords[1] * 100 + bCoords[0] - 1)           #W
        bNeighbours.append((bCoords[1] - 1) * 100 + bCoords[0] - 1)     #NW
        for nID in bNeighbours:
            b = pathfinder.paths.GetUnwalkableByID(nID)
            if b != None:
                b.Discover()

    def Build(self, buildingType):
        if buildingType == enums.BuildingType.KILN_BUILDING:
            self.workTimer = 60
        self.ChangeState(fsm.BuildState(buildingType))

    def SetReturnPath(self):
        pathfinder.pf.Reset()
        self.path = pathfinder.pf.AStar(self.GetTouchingBlock(), self.hubBlock)
        #self.path = self.pathBack
        #self.pathBack = []
        if self.path == type(None):
            print("Return path obstructed???")
            return
        self.ChangeState(fsm.MoveState())
        #print("return path set")

    def GetTouchingBlock(self):
        blockID = int(self.posY / 10) * 100 + (int(self.posX / 10))
        return pathfinder.paths.GetBlockByID(blockID)