import pygame, sys, mapreader
from pygame.locals import *

def StartPygame():
    pygame.init()

    global FPS
    FPS = 60
    global clock
    clock = pygame.time.Clock()

    global maprows
    maprows = mapreader.ReadMap("map.txt")

    displaySize = 1100
    global display
    display = pygame.display.set_mode((displaySize, displaySize))
    display.fill((255,255,255))
    pygame.display.set_caption("Path Finding")
    global rectSize
    rectSize = displaySize / (len(maprows[0]) - 1)


def DrawMap():
    for i in range(len(maprows)):
        #print(i)
        for j in range(len(maprows[i])-1):
            print(j)
            if(maprows[i][j] == "B"):
                pygame.draw.rect(display, (0,0,0), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if (maprows[i][j] == "V"):
                pygame.draw.rect(display, (0,0,255), (j * rectSize, i * rectSize, rectSize, rectSize))
                continue
            #if(maprows[i][j] == "X"):
                #pygame.draw.rect(display, (0,0,0), (j*rectSize, i*rectSize, rectSize, rectSize))
                #pathfinder.paths.pathBlocks.append(pathfinder.PathBlock(i*100+j, neighbours, False, False, False))
            if(maprows[i][j] == "M"):
                pygame.draw.rect(display, (50,150,50), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if(maprows[i][j] == "T"):
                pygame.draw.rect(display, (0,50,0), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if(maprows[i][j] == "G"):
                pygame.draw.rect(display, (101,67,33), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue

def DrawPath(path):
    for i in range(len(path)-1):
        startPoint = (path[i].id%100 + 1)*(rectSize) - rectSize/2, (path[i].id/100 + 1)*(rectSize) - rectSize/2
        endPoint = (path[i+1].id%100 + 1)*(rectSize) - rectSize/2, (path[i+1].id/100 + 1)*(rectSize) - rectSize/2
        pygame.draw.line(display, (0,0,255), startPoint, endPoint, 3)

# def DrawAStar(openList, closedList):
#     for i in range(len(openList)):
#         centerPoint = (openList[i].id%100 + 1)*(rectSize) - rectSize/2, (openList[i].id/100 + 1)*(rectSize) - rectSize/2
#         pygame.draw.circle(display, (255,155,0), centerPoint, 3)
#         if(openList[i].prevBlockID != 0):
#             print(openList[i].prevBlockID)
#             pB = openList[i].GetPrevBlock()
#             x = (((pB.id%100 + 1) - (openList[i].id%100 + 1)) / 2) + (openList[i].id%100 + 1)
#             y = (((pB.id/100 + 1) - (openList[i].id/100 + 1)) / 2) + (openList[i].id/100 + 1)
#             endPoint = (x*rectSize - rectSize/2), (y*rectSize - rectSize/2)
#             pygame.draw.line(display, (0,255,0), centerPoint, endPoint, 2)
#     for i in range(len(closedList)):
#         centerPoint = (closedList[i].id%100 + 1)*rectSize - rectSize/2, (closedList[i].id/100 + 1)*rectSize - rectSize/2
#         pygame.draw.circle(display, (0,255,255), centerPoint, 3)
#         if (closedList[i].prevBlockID != 0):
#             print(closedList[i].prevBlockID)
#             pB = closedList[i].GetPrevBlock()
#             x = (((pB.id % 100 + 1) - (closedList[i].id % 100 + 1)) / 2) + (closedList[i].id % 100 + 1)
#             y = (((pB.id / 100 + 1) - (closedList[i].id / 100 + 1)) / 2) + (closedList[i].id / 100 + 1)
#             endPoint = (x * rectSize - rectSize / 2), (y * rectSize - rectSize / 2)
#             pygame.draw.line(display, (255, 0, 0), centerPoint, endPoint, 2)

def DrawVisited(visited):
    for i in range(len(visited)):
        centerPoint = (visited[i].id%100 + 1)*(rectSize) - rectSize/2, (visited[i].id/100 + 1)*(rectSize) - rectSize/2
        pygame.draw.circle(display, (255,155,0), centerPoint, 3)
        if(visited[i].prevBlockID != 0):
            #print(visited[i].prevBlockID)
            pB = visited[i].GetPrevBlock()
            x = (((pB.id%100 + 1) - (visited[i].id%100 + 1)) / 2) + (visited[i].id%100 + 1)
            y = (((pB.id/100 + 1) - (visited[i].id/100 + 1)) / 2) + (visited[i].id/100 + 1)
            endPoint = (x*rectSize - rectSize/2), (y*rectSize - rectSize/2)
            pygame.draw.line(display, (0,255,0), centerPoint, endPoint, 2)

def Clear():
    display.fill((255,255,255))
    DrawMap()

def Update():
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
