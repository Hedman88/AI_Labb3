import agent, fsm, pathfinder, enums, random

class Overlord:
    agents = []

    def SpawnAgents(self):
        maxAgents = 50
        print(len(pathfinder.paths.pathBlocks))
        startBlock = pathfinder.paths.GetNthBlock(random.randrange(9163))
        for i in range(maxAgents):
            for j in range(len(startBlock.adjacents)):
                rBlock = pathfinder.paths.GetBlockByID(startBlock.adjacents[i])
                self.agents.append(agent.Agent(i, rBlock.IdToCoordinates()))
                self.agents[j].SetHubBlock(startBlock)

        for i in range(len(startBlock.adjacents)):
            rBlock = pathfinder.paths.GetBlockByID(startBlock.adjacents[i])
            for j in range(50):
                self.agents.append(agent.Agent(j, rBlock.IdToCoordinates()))
                self.agents[j].SetHubBlock(startBlock)


    def UpdateAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())

    def OperationCharcoal(self, nrDisc, nrKiln, nrBuild):
        for i in range(len(self.agents)):
            if i < nrDisc:
                self.agents[i].SetGoal(enums.GoalEnum.DISCOVER_GOAL)
            if i < nrDisc + nrKiln:
                self.agents[i].SetGoal(enums.GoalEnum.KILN_GOAL)
            if i < nrDisc + nrKiln + nrBuild:
                self.agents[i].SetGoal(enums.GoalEnum.BUILD_KILNS_GOAL)
            else:
                return

overlord = Overlord()