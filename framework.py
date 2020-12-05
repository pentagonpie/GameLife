import pygame


class cell:
    def __init__(self, x, y):
        assert type(x) == int
        assert type(y) == int
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.x + (self.y * 1000))

    def __eq__(self, other):

        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def getClose(self):
        near = []
        near.append(cell(self.x, self.y - 1))
        near.append(cell(self.x, self.y + 1))
        near.append(cell(self.x - 1, self.y))
        near.append(cell(self.x + 1, self.y))

        near.append(cell(self.x - 1, self.y - 1))
        near.append(cell(self.x + 1, self.y + 1))
        near.append(cell(self.x - 1, self.y + 1))
        near.append(cell(self.x + 1, self.y - 1))
        return near

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def draw(self, screen, location, size):
        color = (0, 0, 0)
        pygame.draw.rect(
            screen, color, [location[0] + 2, location[1] + 2, size - 2, size - 2]
        )


class pivot:
    def __init__(self, coord, aCell, sizeX, sizeY):
        self.mainCell = aCell
        self.coord = [int(coord[0]), int(coord[1])]
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.centerCoord = [coord[0], coord[1]]

    def __str__(self):
        return "({},{})".format(self.mainCell.x, self.mainCell.y)

    def changeCell(self, aCell):
        self.mainCell = aCell

    def updateCenterCoord(self):
        self.centerCoord[0] = self.coord[0]
        self.centerCoord[1] = self.coord[1]

    def updateCoord(self, newCoord):
        self.coord[0] = int(newCoord[0])
        self.coord[1] = int(newCoord[1])

    # print("new pivot coord are {}, {}".format(self.coord[0],self.coord[1]))

    def updateMainCell(self, aCell):
        self.mainCell = aCell

    def coordMove(self, xDelta, yDelta):
        self.updateCoord((self.centerCoord[0] + xDelta, self.centerCoord[1] + yDelta))

    def move(self, start, end, size):
        # print("mouse position is {},{}".format(end[0],end[1]))
        # print("centerCoord are ", self.centerCoord)
        xDelta = end[0] - start[0]
        yDelta = end[1] - start[1]
        # print("moving pivot by {} and {}".format(xDelta,yDelta))
        self.coordMove(xDelta, yDelta)

    # Function to update the pivot cell when he moves from center of screen to a new pivot in the center
    def transformPivot(self, size):
        print("calling transformPivot")
        limit = 120

        centerX = self.sizeX / 2
        centerY = self.sizeY / 2
        maxX = centerX + limit
        maxY = centerY + limit
        minX = centerX - limit
        minY = centerY - limit

        oldX = self.coord[0]
        oldY = self.coord[1]

        # Default of jumps for both x,y are zero, if we get out of center screen will need to update those
        jumpsY = 0
        jumpsX = 0
        needChange = False

        # Check if coordinates get out of center range
        if oldX > maxX or oldX < minX:
            needChange = True
            if oldX > maxX:
                deltaX = maxX - oldX
            elif oldX < minX:
                # positive jump
                deltaX = minX - oldX
            else:
                deltaX = 0

            jumpsX = (deltaX) // size
            if jumpsX < 0:
                jumpsX += -2
            else:
                jumpsX += 2

        # Check if coordinates get out of center range
        if oldY > maxY or oldY < minY:
            needChange = True
            if oldY > maxY:
                deltaY = maxY - oldY
            elif oldY < minY:
                # positive jump
                deltaY = minY - oldY
            else:
                deltaY = 0

            jumpsY = (deltaY) // size
            if jumpsY < 0:
                jumpsX += -2
            else:
                jumpsY += 2

        if needChange:
            # New coordinates of pivot
            x = oldX + jumpsX * size
            # Y is inverted in pygame
            y = oldY + jumpsY * size
            # New values of pivot
            x1 = int(self.mainCell.x + jumpsX)
            y1 = int(self.mainCell.y - jumpsY)

            self.updateCoord([x, y])
            self.changeCell(cell(x1, y1))


class grid:
    # list of living cells in grid, each one in the form (x,y) where x and y are integer number,positive or negative
    def __init__(self):
        self.cells = set()
        self.size = 20
        self.biggestSize = 35
        self.smallestSize = 10
        self.jumpsSize = 5

    def add(self, aCell):
        self.cells.add(aCell)

    def remove(self, aCell):
        self.cells.discard(aCell)

    def getCells(self):
        return self.cells

    def changeSize(self, newSize):
        self.size = newSize

    def update(self):
        toRemove = self.ruleDying()
        toAdd = self.ruleBorn()
        pop = self.cells.discard
        push = self.cells.add

        for x in toRemove:
            pop(x)

        for x in toAdd:
            push(x)

    def zoom(self, zoomIn):
        if zoomIn:
            if self.size < self.biggestSize:
                self.changeSize(self.size + self.jumpsSize)
        else:
            if self.size > self.smallestSize:
                self.changeSize(self.size - self.jumpsSize)

    def ruleBorn(self):
        born = []
        bornPush = born.append

        dead = set()
        for living in self.cells:
            for aCell in living.getClose():
                dead.add(aCell)
        dead.difference(self.cells)

        limit = 50
        for aCell in dead:
            amount = self.getNeighbors(aCell)
            # If 3 neighbors, cell is born, only if not too far away from center
            if amount == 3:
                # control limits for cell in screen
                if aCell.x > limit or aCell.x < -limit:
                    continue
                if aCell.y > limit or aCell.y < -limit:
                    continue

                bornPush(aCell)

        return born

    def exists(self, aCell):
        pass

    def getNeighbors(self, aCell):
        allNear = aCell.getClose()
        amount = 0

        for a in allNear:
            if a in self.cells:
                amount += 1
        return amount

    def ruleDying(self):
        died = []
        diedPush = died.append
        for a in self.cells:
            amount = self.getNeighbors(a)
            if amount > 3:
                diedPush(a)
            elif amount < 2:
                diedPush(a)

        return died
