import agent, fsm, pathfinder, enums, random, time

class Overlord:
    agents = []
    charcoal = 0
    nrDisc = 0
    nrKiln = 0
    nrBuild = 0
    nrIdleKilners = 0

    kilns = []

    foundWood = False

    objectiveCompleted = False
    startTime = 0
    finalTime = 0

    def SpawnAgents(self):
        self.startTime = time.time()
        maxAgents = 50
        startBlock = pathfinder.paths.GetNthBlock(random.randrange(9163))
        startBlock.Discover()
        i = 0
        while i < maxAgents:
            self.agents.append(agent.Agent(i, startBlock.IdToCoordinates()))
            self.agents[i].SetHubBlock(startBlock)
            i += 1
            for j in range(len(startBlock.adjacents)):
                if i >= maxAgents:
                    return
                nBlock = pathfinder.paths.GetBlockByID(startBlock.adjacents[j])
                nBlock.Discover()
                self.agents.append(agent.Agent(i, nBlock.IdToCoordinates()))
                self.agents[i].SetHubBlock(startBlock)
                i += 1


    def UpdateAgents(self):
        if self.objectiveCompleted is False:
            for i in range(len(self.agents)):
                self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].SetGoal(enums.GoalEnum.WOOD_GOAL)
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())

    def OperationCharcoal(self, nrDisc, nrKiln, nrBuild):
        self.nrDisc = nrDisc
        self.nrKiln = nrKiln
        self.nrBuild = nrBuild
        for i in range(len(self.agents)):
            if i < nrDisc:
                self.agents[i].SetGoal(enums.GoalEnum.DISCOVER_GOAL)
            elif i < nrDisc + nrKiln:
                self.agents[i].SetGoal(enums.GoalEnum.KILN_GOAL)
                self.nrIdleKilners += 1
            elif i < nrDisc + nrKiln + nrBuild:
                self.agents[i].SetGoal(enums.GoalEnum.BUILD_KILNS_GOAL)
            else:
                return

    def SetKilnerToWorkplace(self, building):
        if self.nrIdleKilners <= 0:
            print("Need more kilners")
        else:
            for i in range(self.nrDisc, self.nrDisc + self.nrKiln):
                if self.agents[i].workPlace == 0:
                    self.agents[i].AddWorkPlace(self.kilns.pop())
                    return

    def AddCharcoal(self):
        self.charcoal += 1
        if self.charcoal >= 200 and self.objectiveCompleted is False:
            self.objectiveCompleted = True
            self.finalTime = time.time() - self.startTime

    def AddKiln(self, kiln):
        self.kilns.append(kiln)
        self.SetKilnerToWorkplace(kiln)

overlord = Overlord()