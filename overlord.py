import agent, fsm, pathfinder

class Overlord:
    agents = []

    def SpawnAgents(self):
        self.agents.append(agent.Agent(0, (41, 49)))
        hubBlock = self.agents[0].hubBlock
        for i in range(49):
            rBlock = pathfinder.paths.GetRandomBlock()
            self.agents.append(agent.Agent(i+1, rBlock.IdToCoordinates()))
            self.agents[i+1].SetHubBlock(hubBlock)

    def UpdateAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())


overlord = Overlord()