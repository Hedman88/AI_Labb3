import enums, pathfinder, random, buildings, overlord

class IdleState:
    def Execute(self, agent):
        agent.FindTask()
        return

class MoveState:
    currentGoal = 0
    dirX = 0
    dirY = 0
    def Execute(self, agent):
        if(self.currentGoal == 0):
            self.currentGoal = agent.path.pop()
            agent.pathBack.append(self.currentGoal)
            self.dirX = self.currentGoal.id % 100 - agent.GetTouchingBlock().id % 100
            self.dirY = int(self.currentGoal.id / 100) - int(agent.GetTouchingBlock().id / 100)
        if((self.currentGoal.id%100) * 10 + 5 == int(agent.posX) and int(self.currentGoal.id/100) * 10 + 5 == int(agent.posY)):
            if agent.path != []:
                self.currentGoal = agent.path.pop()
                agent.pathBack.append(self.currentGoal)
            else:
                if(agent.goal == enums.GoalEnum.WOOD_GOAL):
                    if agent.holding == enums.ItemEnum.NONE:
                        agent.ChangeState(WoodChoppingState())
                        return
                    else:
                        agent.DropItem()
                        agent.FindWood()
                        return
                agent.ChangeState(IdleState())
                return
            self.dirX = self.currentGoal.id%100 - agent.GetTouchingBlock().id%100
            self.dirY = int(self.currentGoal.id/100) - int(agent.GetTouchingBlock().id/100)
        agent.Move(self.currentGoal.ms, self.dirX, self.dirY)

class WoodChoppingState:
    def Execute(self, agent):
        if agent.GetTouchingBlock().hasTrees:
            if agent.workTimer <= 0:
                agent.workTimer = 30
                agent.GetTouchingBlock().RemoveTree()
                agent.PickUpItem()
                agent.SetReturnPath()
            else:
                agent.workTimer -= 1
        else:
            if(agent.goal == enums.GoalEnum.WOOD_GOAL):
                agent.FindWood()
                agent.ChangeState(MoveState())

class UpgradeState:
    def __init__(self, upgradeType):
        self.upgradeType = upgradeType

    def Execute(self, agent):
        if agent.upgradeTimer > 0:
            agent.upgradeTimer -= 1
        else:
            agent.type = self.upgradeType
            agent.ChangeState(IdleState())
            print("Upgrade complete!", agent.ID, "is now a", agent.type)

class ExploreState:
    currentGoal = 0
    dirX = 0
    dirY = 0
    ms = 1
    def Execute(self, agent):
        if agent.type != enums.AgentType.DISCOVERER:
            print(agent.ID, "is not a discoverer!!!")
            agent.ChangeState(IdleState())
        if self.currentGoal == 0:
            self.currentGoal = agent.GetTouchingBlock()
        if (self.currentGoal.id % 100) * 10 + 5 == int(agent.posX) and int(self.currentGoal.id / 100) * 10 + 5 == int(agent.posY):
            agent.DiscoverTiles()
            mostFogged = 0
            currentBlock = agent.GetTouchingBlock()
            self.ms = currentBlock.ms
            if currentBlock.walkable is False:
                print("CURRENTBLOCK IS NOT WALKABLE")
            for n in currentBlock.adjacents:
                xFogged = 0
                nBlock = pathfinder.paths.GetBlockByID(n)
                for nn in nBlock.adjacents:
                    if pathfinder.paths.GetBlockByID(nn).isFogged:
                        xFogged += 1
                if mostFogged < xFogged:
                    mostFogged = xFogged
                    self.currentGoal = nBlock
            if mostFogged == 0:
                x = len(currentBlock.adjacents)
                randNeighbour = random.randrange(x)
                self.currentGoal = pathfinder.paths.GetBlockByID(currentBlock.adjacents[randNeighbour])

            self.dirX = self.currentGoal.id % 100 - agent.GetTouchingBlock().id % 100
            self.dirY = int(self.currentGoal.id / 100) - int(agent.GetTouchingBlock().id / 100)

        agent.Move(self.ms, self.dirX, self.dirY)

class RunKilnState:
    def Execute(self, agent):
        if len(agent.workPlace.block.kilns) < overlord.overlord.nrKiln:
            return
        if agent.workTimer == 0:
            agent.workPlace.BurnWood()
            agent.workTimer = 30
        elif agent.hubBlock.woodPile < 2:
            #print("Not enough wood to burn")
            return
        else:
            agent.workTimer -= 1

class BuildState:
    def __init__(self, buildingType):
        self.buildingType = buildingType

    def Execute(self, agent):
        if agent.workTimer == 0:
            b = agent.GetTouchingBlock()
            for i in range(10):
                b.TakeWood()

            building = buildings.Building(self.buildingType, b)
            b.kilns.append(building)
            if building.type == enums.BuildingType.KILN_BUILDING:
                overlord.overlord.AddKiln(building)

            agent.ChangeState(IdleState())
            print("Kiln built")
        else:
            agent.workTimer -= 1