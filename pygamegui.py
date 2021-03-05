import pygame, sys, mapreader, overlord, pathfinder, random
from pygame.locals import *

def StartPygame():
    pygame.init()

    global FPS
    FPS = 60
    global clock
    clock = pygame.time.Clock()

    global maprows
    maprows = mapreader.ReadMap("map.txt")

    displaySize = 1000
    global display
    display = pygame.display.set_mode((displaySize, displaySize))
    display.fill((255,255,255))
    pygame.display.set_caption("Path Finding")
    global rectSize
    rectSize = displaySize / (len(maprows[0]) - 1)

    global treeRand
    treeRand = []
    for i in range(5):
        treeRand.append(random.randrange(3))

def DrawMap():
    for i in range(len(maprows)):
        for j in range(len(maprows[i])-1):
            if(maprows[i][j] == "B"):
                pygame.draw.rect(display, (0,0,0), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if (maprows[i][j] == "V"):
                pygame.draw.rect(display, (0,0,255), (j * rectSize, i * rectSize, rectSize, rectSize))
                continue
            if(maprows[i][j] == "M"):
                pygame.draw.rect(display, (50,150,50), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if(maprows[i][j] == "T"):
                pygame.draw.rect(display, (50,150,50), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue
            if(maprows[i][j] == "G"):
                pygame.draw.rect(display, (101,67,33), (j*rectSize, i*rectSize, rectSize, rectSize))
                continue

def DrawBlocks():
    blocks = pathfinder.paths.pathBlocks
    for key in blocks:
        b = blocks[key]
        if(b.hasTrees):
            pygame.draw.rect(display, (0, 50, 0), ((b.id%100) * rectSize, int(b.id/100) * rectSize, rectSize, rectSize))
            for i in range(b.trees):
                pygame.draw.rect(display, (101, 67, 33), ((b.id % 100) * rectSize + treeRand[i]*i, int(b.id / 100) * rectSize + 2*i, 2, 2))
        if b.hasWood:
            pygame.draw.rect(display, (101, 67, 33), ((b.id % 100) * rectSize + 5, int(b.id / 100) * rectSize + 5, 2, 2))

def DrawPath(path):
    for i in range(len(path)-1):
        startPoint = (path[i].id%100 + 1)*(rectSize) - rectSize/2, (path[i].id/100 + 1)*(rectSize) - rectSize/2
        endPoint = (path[i+1].id%100 + 1)*(rectSize) - rectSize/2, (path[i+1].id/100 + 1)*(rectSize) - rectSize/2
        pygame.draw.line(display, (0,0,255), startPoint, endPoint, 3)

def DrawAgents(agents):
    for i in range(len(agents)):
        point = (agents[i].posX, agents[i].posY)
        pygame.draw.rect(display, (255,0,0), (agents[i].posX, agents[i].posY, 3, 3))

def Clear():
    display.fill((255,255,255))
    DrawMap()

def Update():
    Clear()
    DrawBlocks()
    DrawAgents(overlord.overlord.agents)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
