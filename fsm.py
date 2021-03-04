
class IdleState:
    def Execute(self, agent):
        return

class MoveState:
    currentGoal = 0
    dirX = 0
    dirY = 0
    def Execute(self, agent):
        if(self.currentGoal == 0):
            self.currentGoal = agent.path.pop()
        if((self.currentGoal.id%100) * 10 + 5 == int(agent.posX) and int(self.currentGoal.id/100) * 10 + 5 == int(agent.posY)):
            if agent.path != []:
                self.currentGoal = agent.path.pop()
            else:
                agent.ChangeState(IdleState())
                return
            self.dirX = self.currentGoal.id%100 - agent.GetTouchingBlock().id%100
            self.dirY = int(self.currentGoal.id/100) - int(agent.GetTouchingBlock().id/100)
        agent.Move(self.currentGoal.ms, self.dirX, self.dirY)