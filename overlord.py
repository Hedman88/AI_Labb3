import agent, fsm

class Overlord:
    agents = []

    def SpawnAgents(self):
        for i in range(1):
            self.agents.append(agent.Agent(i, (41,49)))

    def UpdateAgents(self):
        for i in range(len(self.agents)):
            self.agents[i].Update()

    def GetWood(self):
        for i in range(len(self.agents)):
            if(type(self.agents[i].state) == type(fsm.IdleState())):
                self.agents[i].FindWood()
                self.agents[i].ChangeState(fsm.MoveState())


overlord = Overlord()