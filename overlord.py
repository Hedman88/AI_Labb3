import agent, fsm, pathfinder, enums, random

class Overlord:
    agents = []

    def SpawnAgents(self):
        maxAgents = 50
        print(len(pathfinder.paths.pathBlocks))
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
        for i in range(len(self.agents)):
            self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].SetGoal(enums.GoalEnum.WOOD_GOAL)
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())

    def OperationCharcoal(self, nrDisc, nrKiln, nrBuild):
        for i in range(len(self.agents)):
            if i < nrDisc:
                self.agents[i].SetGoal(enums.GoalEnum.DISCOVER_GOAL)
            elif i < nrDisc + nrKiln:
                self.agents[i].SetGoal(enums.GoalEnum.KILN_GOAL)
            elif i < nrDisc + nrKiln + nrBuild:
                self.agents[i].SetGoal(enums.GoalEnum.BUILD_KILNS_GOAL)
            else:
                return

overlord = Overlord()