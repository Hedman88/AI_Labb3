import pygamegui as gui
import time, math


class PathFinder:
    goalFound = False
    visited = []
    path = []

    # Resets all values so the next run wont be affected by the previous one
    def Reset(self):
        self.visited = []
        self.path = []
        self.goalFound = False

    def bfs(self, startBlock):
        self.visited.append(startBlock)
        bfsQ = []
        bfsQ.append(startBlock)
        while bfsQ:
            s = bfsQ.pop(0)
            for neighbour in s.adjacents:
                neighbourBlock = paths.GetBlockByID(neighbour)
                if neighbourBlock not in self.visited:
                    self.visited.append(neighbourBlock)
                    bfsQ.append(neighbourBlock)
                    neighbourBlock.prevBlockID = s.id
                    if (neighbourBlock.isGoal):
                        self.path.append(neighbourBlock)
                        prevID = neighbourBlock.prevBlockID
                        while (prevID != 0):
                            prevBlock = paths.GetBlockByID(prevID)
                            self.path.append(prevBlock)
                            prevID = prevBlock.prevBlockID
                        return
            # gui.Clear()
            # gui.DrawVisited(self.visited)
            # gui.Update()
            # time.sleep(0.01)

    def AStar(self, startBlock):
        openList = []
        closedList = []
        openList.append(startBlock)

        while openList:
            q = openList[0]
            # find best block by f value
            for i in range(len(openList)):
                if (q.f > openList[i].f):
                    q = openList[i]
            openList.remove(q)
            # go through all successors
            for neighbourID in q.adjacents:
                skip = False
                neighbourBlock = paths.GetBlockByID(neighbourID)

                if (neighbourBlock.isGoal):
                    self.path.append(neighbourBlock)
                    prevID = q.prevBlockID
                    while (prevID != 0):
                        prevBlock = paths.GetBlockByID(prevID)
                        self.path.append(prevBlock)
                        prevID = prevBlock.prevBlockID
                    return
                if (neighbourBlock.id % 100 != q.id % 100 and neighbourBlock.id / 100 != q.id / 100):
                    neighbourBlock.g = 1.4
                    # Byt till denna undre rad för fullständig A*
                    # neighbourBlock.g = q.g + 1.4
                else:
                    neighbourBlock.g = 1
                    # Byt till denna undre rad för fullständig A*
                    # neighbourBlock.g = q.g + 1
                neighbourBlock.h = self.Diagonal(neighbourID)
                neighbourBlock.f = neighbourBlock.g + neighbourBlock.h
                for i in openList:
                    if (i.id == neighbourBlock.id and neighbourBlock.f >= i.f):
                        skip = True
                for i in closedList:
                    if (i.id == neighbourBlock.id and neighbourBlock.f >= i.f):
                        skip = True
                if skip is False:
                    # set q as parent to all neighbour blocks
                    neighbourBlock.prevBlockID = q.id
                    openList.append(neighbourBlock)
            closedList.append(q)
            # gui.Clear()
            # gui.DrawAStar(openList, closedList)
            # gui.Update()
            # time.sleep(0.01)

    # Following are different heuristics for testing purposes
    def Manhattan(self, currentID):
        xCur = currentID % 100
        yCur = currentID / 100
        # Converting ID to coordinates
        goalID = paths.GetGoal().id
        xGoal = goalID % 100
        yGoal = goalID / 100
        h = abs(xCur - xGoal) + abs(yCur - yGoal)
        return h

    def Diagonal(self, currentID):
        xCur = currentID % 100
        yCur = currentID / 100
        # Converting ID to coordinates
        goalID = paths.GetGoal().id
        xGoal = goalID % 100
        yGoal = goalID / 100
        # Diagonal Distance Heuristics
        h = max([abs(xCur - xGoal), abs(yCur - yGoal)])
        return h

    def Euclidean(self, currentID):
        xCur = currentID % 100
        yCur = currentID / 100
        # Converting ID to coordinates
        goalID = paths.GetGoal().id
        xGoal = goalID % 100
        yGoal = goalID / 100

        h = math.sqrt((xCur - xGoal) ** 2 + (yCur - yGoal) ** 2)
        return h


class PathBlock:
    prevBlockID = 0
    # A* values
    g = 0.0
    h = 0.0
    f = 0.0

    isFogged = True
    def __init__(self, ID, adjacents, ms, hasTrees):
        self.id = ID
        self.adjacents = adjacents
        self.ms = ms  # 1 for mark and 0.5 for trees and sumpmark
        self.hasTrees = hasTrees
        if(self.hasTrees):
            self.trees = 5

    def GetPrevBlock(self):
        return paths.GetBlockByID(self.prevBlockID)


class Paths:
    pathBlocks = {}

    def GetStart(self):
        return self.pathBlocks.get("start")

    def GetGoal(self):
        return self.pathBlocks.get("goal")

    def GetBlockByID(self, ID):
        return self.pathBlocks.get(ID)


paths = Paths()
pf = PathFinder()
