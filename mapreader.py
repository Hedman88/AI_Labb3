import pathfinder

def ReadMap(mapFileName):
    f = open(mapFileName, "r")
    global maprows
    maprows = f.readlines()
    f.close()
    return maprows

# Creating all map nodes and storing their IDs and neighbour IDs as ints
# by taking Y-coordinate times 100 and adding the X-coordinate to that
def InitMapBlocks():
    print(len(maprows))
    for i in range(len(maprows)):
        for j in range(len(maprows[i]) - 1):
            selfID = i * 100 + j
            # All neighbouring IDs
            N = (i - 1) * 100 + j
            NE = (i - 1) * 100 + j + 1
            E = i * 100 + j + 1
            SE = (i + 1) * 100 + j + 1
            S = (i + 1) * 100 + j
            SW = (i + 1) * 100 + j - 1
            W = i * 100 + j - 1
            NW = (i - 1) * 100 + j - 1
            # SE, S, E, N, NW, W, SW, NE best order?
            neighbours = []
            if (maprows[i][j] == "B" or maprows[i][j] == "V"):
                continue

            # Appending all relevant IDs to current block
            if (maprows[i - 1][j] != "B" and maprows[i - 1][j] != "V"):
                neighbours.append(N)

            if (maprows[i - 1][j + 1] != "B" and maprows[i - 1][j + 1] != "V") and \
                    (maprows[i - 1][j] != "B" and maprows[i - 1][j] != "V") and \
                    (maprows[i][j + 1] != "B" and maprows[i][j + 1] != "V"):
                neighbours.append(NE)

            if (maprows[i][j + 1] != "B" and maprows[i][j + 1] != "V"):
                neighbours.append(E)

            if (maprows[i + 1][j + 1] != "B" and maprows[i + 1][j + 1] != "V") and \
                    (maprows[i][j + 1] != "B" and maprows[i][j + 1] != "V") and \
                    (maprows[i + 1][j] != "B" and maprows[i + 1][j] != "V"):
                neighbours.append(SE)

            if (maprows[i + 1][j] != "B" and maprows[i + 1][j] != "V"):
                neighbours.append(S)

            if (maprows[i + 1][j - 1] != "B" and maprows[i + 1][j - 1] != "V") and \
                    (maprows[i + 1][j] != "B" and maprows[i + 1][j] != "V") and \
                    (maprows[i][j - 1] != "B" and maprows[i][j - 1] != "V"):
                neighbours.append(SW)

            if (maprows[i][j - 1] != "B" and maprows[i][j - 1] != "V"):
                neighbours.append(W)

            if (maprows[i - 1][j - 1] != "B" and maprows[i - 1][j - 1] != "V") and \
                    (maprows[i][j - 1] != "B" and maprows[i][j - 1] != "V") and \
                    (maprows[i - 1][j] != "B" and maprows[i - 1][j] != "V"):
                neighbours.append(NW)

            # Mark
            if (maprows[i][j] == "M"):
                pathfinder.paths.pathBlocks[selfID] = pathfinder.PathBlock(selfID, neighbours, 1, False)
            # Sumpmark
            if(maprows[i][j] == "G"):
                pathfinder.paths.pathBlocks[selfID] = pathfinder.PathBlock(selfID, neighbours, 0.5, False)
            # Träd
            if (maprows[i][j] == "T"):
                block = pathfinder.PathBlock(selfID, neighbours, 0.5, True)
                pathfinder.paths.pathBlocks[selfID] = block