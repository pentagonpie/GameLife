import pygame
import random
from datetime import datetime
import time
from structures import button

class cell:
    def __init__(self,x,y):
        assert type(x) == int
        assert type(y) == int
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.x+(self.y*1000))
        

    def __eq__(self,other):
        #print("using eq~~")
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def getClose(self):
        near = []
        near.append(cell(self.x,self.y-1))
        near.append(cell(self.x,self.y+1))
        near.append(cell(self.x-1,self.y))
        near.append(cell(self.x+1,self.y))

        near.append(cell(self.x-1,self.y-1))
        near.append(cell(self.x+1,self.y+1))
        near.append(cell(self.x-1,self.y+1))
        near.append(cell(self.x+1,self.y-1))
      #  print("all close are ", near)
        return near


    def __str__(self):
        return '({},{})'.format(self.x,self.y)


    

    def draw(self,screen,location, size):
        color = (0,0,0)
        pygame.draw.rect(screen,color,[location[0]+2, location[1]+2, size-2, size-2]) 
   

    
    
class pivot:
    def __init__(self,coord, aCell):
        self.mainCell = aCell
        self.coord = [int(coord[0]),int(coord[1])]
        
        self.centerCoord = [coord[0],coord[1]]


    def __str__(self):
        return '({},{})'.format(self.mainCell.x,self.mainCell.y)

    def changeCell(self,aCell):
        self.mainCell = aCell


    def updateCenterCoord(self):
        self.centerCoord[0] = self.coord[0]
        self.centerCoord[1] = self.coord[1]

    def updateCoord(self,newCoord):
        self.coord[0] = int(newCoord[0])
        self.coord[1] = int(newCoord[1])
       # print("new pivot coord are {}, {}".format(self.coord[0],self.coord[1]))


    def updateMainCell(self,aCell):
        self.mainCell = aCell

    def coordMove(self,xDelta,yDelta):
        self.updateCoord((self.centerCoord[0]+xDelta, self.centerCoord[1]+yDelta))



    def move(self,start ,end,size):
        #print("mouse position is {},{}".format(end[0],end[1]))
        #print("centerCoord are ", self.centerCoord)
        xDelta = end[0]-start[0]
        yDelta = end[1]-start[1]
        #print("moving pivot by {} and {}".format(xDelta,yDelta))
        self.coordMove(xDelta,yDelta)
        
    #Function to update the pivot cell when he moves from center of screen to a new pivot in the center
    def transformPivot(self,size):
        print("calling transformPivot")
        limit = 120
        global sizeX
        global sizeY

        centerX = sizeX/2
        centerY = sizeY/2
        maxX = centerX+limit
        maxY = centerY+limit
        minX = centerX-limit
        minY = centerY-limit

        oldX = self.coord[0]
        oldY = self.coord[1]


        #Default of jumps for both x,y are zero, if we get out of center screen will need to update those
        jumpsY = 0
        jumpsX = 0
        needChange=False


        #Check if coordinates get out of center range
        if oldX > maxX or oldX < minX:
            needChange=True
            if oldX > maxX:
                deltaX = maxX-oldX
            elif oldX<minX:
                #positive jump
                deltaX = minX-oldX
            else:
                deltaX=0

            jumpsX = (deltaX)//size
            if jumpsX<0:
                jumpsX += -2
            else:
                jumpsX += 2


        #Check if coordinates get out of center range
        if oldY > maxY or oldY < minY:
            needChange=True
            if oldY > maxY:
                deltaY = maxY-oldY
            elif oldY<minY:
                #positive jump
                deltaY = minY-oldY
            else:
                deltaY = 0

            jumpsY = (deltaY)//size
            if jumpsY<0:
                jumpsX += -2
            else:
                jumpsY += 2


        if needChange:
            #New coordinates of pivot
            x = oldX+jumpsX*size
            #Y is inverted in pygame
            y = oldY+jumpsY*size
            #New values of pivot
            x1 = int(self.mainCell.x+jumpsX)
            y1 = int(self.mainCell.y -jumpsY)

            self.updateCoord([x,y])
            self.changeCell(cell(x1,y1))

        




def printScreen(screen,sizeX,sizeY,aGrid,thePivot,buttons):
    
    movement = aGrid.size
    screen.fill((241,248,242))
    offset = 120
    color = (130, 12, 255)
    color2 = (230, 60, 90)
    thickness = 2
    size = int(sizeX/movement)
    amount = size*3

    #Vertical lines
    for x in range(-amount,amount):
        #                     start      x         y   end      x       y
        pygame.draw.line(screen,color,(movement*x+thePivot.coord[0], 0),    (movement*x+thePivot.coord[0],sizeY),thickness)

    #Horizontal lines
    for x in range(-amount,amount):
        #                     start    x      y      end      x       y
        pygame.draw.line(screen,color,(0,movement*x+thePivot.coord[1]),    (sizeX,movement*x+thePivot.coord[1]),thickness)

    for aCell in aGrid.getCells():
        location = computeCoord(thePivot,aCell,movement)
        if insideScreen(location,sizeX,sizeY,movement):
            aCell.draw(screen,location, movement)

    #Temporary, only to show the pivot location for debugging
    pygame.draw.line(screen,color2,(0,thePivot.coord[1]),    (sizeX,thePivot.coord[1]),3)
    pygame.draw.line(screen,color2,(thePivot.coord[0],0), (thePivot.coord[0],sizeY),3)

    for aButton in buttons:
        if aButton.visible:
            aButton.draw(screen)

    #pygame.draw.rect(screen, boldColor, [movement,44,sizeX-offset*2+55,movement*9+5],5)

#Returns true if coordinates are inside window
def insideScreen(coord,sizeX,sizeY,size):
    #Check if x,y values are bigger than screen size,or smaller than begining of screen minus cell size
    if coord[0] > sizeX or coord[0] <-size:
        return False
    if coord[1] > sizeY or coord[1] <-size:
        return False

    return True
        
#Function used to compute the coordinates of a living cell in the grid relative to a pivot cell
def computeCoord(aPivot,aCell,size):
    border = 2
    xDelta = (aCell.x-aPivot.mainCell.x)*size
    yDelta = (aCell.y-aPivot.mainCell.y)*size

    x = int(aPivot.coord[0] + xDelta)
    y = int(aPivot.coord[1] - yDelta)
    

    return (x,y)

class grid:
    #list of living cells in grid, each one in the form (x,y) where x and y are integer number,positive or negative
    def __init__(self):
        self.cells = set()
        self.size = 25

    def add(self,aCell):
        self.cells.add(aCell)

    def remove(self,aCell):
        self.cells.discard(aCell)

    def getCells(self):
        return self.cells

    def changeSize(self,newSize):
        self.size = newSize

    def update(self):
        startTime = time.time()
        toRemove = self.ruleDying()
        toAdd = self.ruleBorn()
        pop = self.cells.discard
        push = self.cells.add

        for x in toRemove:
            pop(x)
           

        for x in toAdd:
            push(x)
            

        return time.time() - startTime




    def ruleBorn(self):
        born = []
        bornPush = born.append

        dead = set()
        for living in self.cells:
            for aCell in living.getClose():
                dead.add(aCell)
        dead.difference(self.cells)



        limit =50
        for aCell in dead:
            amount = self.getNeighbors(aCell)
            #If 3 neighbors, cell is born, only if not too far away from center
            if amount == 3:
                #control limits for cell in screen
                if aCell.x > limit or aCell.x < -limit:
                    continue
                if aCell.y > limit or aCell.y < -limit:
                    continue
                 
                bornPush(aCell)
             
        return born
        
    def exists(self,aCell):
        pass
        
    def getNeighbors(self,aCell):
        allNear = aCell.getClose()
        amount=0
        
        for a in allNear:
            if a in self.cells:
                amount+=1
        return amount


    def ruleDying(self):
        died = []
        diedPush = died.append
        for a in self.cells:
            amount = self.getNeighbors(a)
            if amount > 3:
                diedPush(a)
            elif amount <2:
                diedPush(a)

        return died


def getCellPressed(myPivot,mouse,size):
    xDelta = (mouse[0]-myPivot.coord[0])/size
    yDelta = (mouse[1]-myPivot.coord[1])/size

    x = int(myPivot.mainCell.x + xDelta)
    y = int(myPivot.mainCell.y - yDelta)

    return cell(x,y)


def pressPlay(button):
    if button.text == "Pause":
        button.text = "Play"

    else:
        button.text = "Pause"
    

def getRandomCells():
    limit = 27
    cells = []
    for x in range(400):
        x = random.choice(range(-limit,limit))
        y = random.choice(range(-limit,limit))
        cells.append(cell(x,y))
        #print("created random cell {},{}".format(x,y))

    return cells

def gliderGun():
    cells = []
    cells.append(cell(17,2))
    cells.append(cell(17,1))
    cells.append(cell(16,2))
    cells.append(cell(16,1))

    cells.append(cell(-17,1))
    cells.append(cell(-17,0))
    cells.append(cell(-18,1))
    cells.append(cell(-18,0))

    cells.append(cell(6,3))
    cells.append(cell(6,4))
    cells.append(cell(6,-1))
    cells.append(cell(6,-2))
    cells.append(cell(4,3))
    cells.append(cell(4,-1))

    cells.append(cell(3,2))
    cells.append(cell(3,1))
    cells.append(cell(3,0))
    cells.append(cell(2,2))
    cells.append(cell(2,1))
    cells.append(cell(2,0))

    cells.append(cell(-1,-1))
    cells.append(cell(-2,0))
    cells.append(cell(-2,-1))
    cells.append(cell(-2,-2))
    cells.append(cell(-3,1))
    cells.append(cell(-3,-3))
    cells.append(cell(-4,-1))
    cells.append(cell(-5,2))
    cells.append(cell(-5,-4))
    cells.append(cell(-6,2))
    cells.append(cell(-6,-4))
    cells.append(cell(-7,1))
    cells.append(cell(-7,-3))
    cells.append(cell(-8,0))
    cells.append(cell(-8,-1))
    cells.append(cell(-8,-2))
    return cells


pygame.init()
sizeX=700
sizeY=700


#cells = getRandomCells()
cells = gliderGun()


mygrid = grid()
mygrid.changeSize(15)
myPivot = pivot((sizeX/2,sizeY/2),cell(0,0))


for aCell in cells:
    mygrid.add(aCell)

#Controls whether the simulation is on or off
play = False


drag = False
timer = 0
screen = pygame.display.set_mode((sizeX,sizeY))
clock = pygame.time.Clock()

UPDATE_EVENT = pygame.USEREVENT+1
pygame.time.set_timer(UPDATE_EVENT, 100)
buttons = []

color1=(74,140,240)
buttonPlay = button(color1, [sizeX-100,sizeY-100], [90,50], "Play")
buttons.append(buttonPlay)

LEFT = 1
RIGHT = 3
MOVE_EVENT = pygame.USEREVENT+2
pygame.time.set_timer(MOVE_EVENT, 70)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #left click is for moving or pressing buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if event.button == LEFT:
                if buttonPlay.collidePoint(mouse):
                    play = not play
                    pressPlay(buttonPlay)

                else:
                    start = mouse
                    myPivot.updateCenterCoord()
                    drag = True

        #Right click is for drawing cells
            elif event.button == RIGHT:
                #cannot draw when mouse on button
                if not buttonPlay.collidePoint(mouse):
                    mouse = pygame.mouse.get_pos()
                    pressedCell = getCellPressed(myPivot,mouse,mygrid.size)
                    mygrid.add(pressedCell)

        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            drag = False
            myPivot.transformPivot(mygrid.size)

        if event.type == MOVE_EVENT and drag:
            end = pygame.mouse.get_pos()
            myPivot.move(start,end, mygrid.size)

        if event.type == UPDATE_EVENT and play:
            mygrid.update()




    printScreen(screen,sizeX,sizeY,mygrid,myPivot,buttons)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(40)