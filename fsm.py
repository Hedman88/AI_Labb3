import enums

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
            agent.pathBack.append(self.currentGoal)
        if((self.currentGoal.id%100) * 10 + 5 == int(agent.posX) and int(self.currentGoal.id/100) * 10 + 5 == int(agent.posY)):
            if agent.path != []:
                self.currentGoal = agent.path.pop()
                agent.pathBack.append(self.currentGoal)
            else:
                print(agent.goal)
                if(agent.goal == enums.GoalEnum.WOOD_GOAL):
                    if agent.holding == enums.ItemEnum.NONE:
                        agent.ChangeState(WoodChoppingState())
                        return
                    else:
                        agent.DropItem()
                        agent.FindWood()
                        agent.ChangeState(MoveState())
                        return
                agent.ChangeState(IdleState())
                return
            self.dirX = self.currentGoal.id%100 - agent.GetTouchingBlock().id%100
            self.dirY = int(self.currentGoal.id/100) - int(agent.GetTouchingBlock().id/100)
        agent.Move(self.currentGoal.ms, self.dirX, self.dirY)

class WoodChoppingState:
    def Execute(self, agent):
        if agent.GetTouchingBlock().hasTrees:
            if agent.woodChopTimer <= 0:
                print("chopped tree")
                agent.woodChopTimer = 30
                agent.GetTouchingBlock().RemoveTree()
                agent.PickUpItem()
                agent.SetReturnPath()
                agent.ChangeState(MoveState())
            else:
                agent.woodChopTimer -= 1
                # if agent.woodChopTimer%5 == 0:
                #     print(agent.woodChopTimer)
        else:
            print("This tile has no trees!!!")
            if(agent.goal == enums.GoalEnum.WOOD_GOAL):
                agent.FindWood()
                agent.ChangeState(MoveState())

class UpgradeState:
    def __init__(self, upgradeType):
        self.upgradeType = upgradeType

    #def Execute(self, agent):
