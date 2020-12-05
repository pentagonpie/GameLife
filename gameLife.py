import pygame
import random
from datetime import datetime
import time
from structures import button
from framework import grid
from framework import pivot
from framework import cell
import shapes


def printScreen(screen, sizeX, sizeY, aGrid, thePivot, buttons):

    movement = aGrid.size
    screen.fill((241, 248, 242))
    offset = 120
    color = (130, 12, 255)
    color2 = (230, 60, 90)
    thickness = 2
    size = int(sizeX / movement)
    amount = size * 3

    # Vertical lines
    for x in range(-amount, amount):
        #                     start      x         y   end      x       y
        pygame.draw.line(
            screen,
            color,
            (movement * x + thePivot.coord[0], 0),
            (movement * x + thePivot.coord[0], sizeY),
            thickness,
        )

    # Horizontal lines
    for x in range(-amount, amount):
        #                     start    x      y      end      x       y
        pygame.draw.line(
            screen,
            color,
            (0, movement * x + thePivot.coord[1]),
            (sizeX, movement * x + thePivot.coord[1]),
            thickness,
        )

    for aCell in aGrid.getCells():
        location = computeCoord(thePivot, aCell, movement)
        if insideScreen(location, sizeX, sizeY, movement):
            aCell.draw(screen, location, movement)

    # Temporary, only to show the pivot location for debugging
    # pygame.draw.line(screen,color2,(0,thePivot.coord[1]),    (sizeX,thePivot.coord[1]),3)
    # pygame.draw.line(screen,color2,(thePivot.coord[0],0), (thePivot.coord[0],sizeY),3)

    for aButton in buttons:
        if aButton.visible:
            aButton.draw(screen)

    # pygame.draw.rect(screen, boldColor, [movement,44,sizeX-offset*2+55,movement*9+5],5)


# Returns true if coordinates are inside window
def insideScreen(coord, sizeX, sizeY, size):
    # Check if x,y values are bigger than screen size,or smaller than begining of screen minus cell size
    if coord[0] > sizeX or coord[0] < -size:
        return False
    if coord[1] > sizeY or coord[1] < -size:
        return False

    return True


# Function used to compute the coordinates of a living cell in the grid relative to a pivot cell
def computeCoord(aPivot, aCell, size):
    border = 2
    xDelta = (aCell.x - aPivot.mainCell.x) * size
    yDelta = (aCell.y - aPivot.mainCell.y) * size

    x = int(aPivot.coord[0] + xDelta)
    y = int(aPivot.coord[1] - yDelta)

    return (x, y)


# from mouse click position get the values of the cell that was at that location
def getCellPressed(myPivot, mouse, size):
    xDelta = (mouse[0] - 7 - myPivot.coord[0]) / size
    yDelta = (mouse[1] - 10 - myPivot.coord[1]) / size

    x = int(myPivot.mainCell.x + xDelta)
    y = int(myPivot.mainCell.y - yDelta)

    return cell(x, y)


def pressPlay(button):
    if button.text == "Pause":
        button.text = "Play"

    else:
        button.text = "Pause"


# Check if any button was pressed
def pressedButton(buttons, mouse):
    for button in buttons:
        if button.collidePoint(mouse):
            return True

    return False


pygame.init()
pygame.display.set_caption("Game Of Life")
sizeX = 700
sizeY = 700


cells = shapes.gliderGun()


mygrid = grid()
mygrid.changeSize(15)
myPivot = pivot((sizeX / 2, sizeY / 2), cell(0, 0), sizeX, sizeY)


for aCell in cells:
    mygrid.add(aCell)

# Controls whether the simulation is on or off
play = False


dragMove = False
dragDraw = False
timer = 0
screen = pygame.display.set_mode((sizeX, sizeY))
clock = pygame.time.Clock()

UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_EVENT, 100)
buttons = []

color1 = (74, 140, 240)
buttonPlay = button(color1, [sizeX - 100, sizeY - 100], [65, 50], "Play")
buttonZoomIn = button(color1, [sizeX - 80, sizeY - 150], [45, 35], "+")
buttonZoomIn.fontSize = 35
buttonZoomOut = button(color1, [sizeX - 80, sizeY - 200], [45, 35], "-")
buttonZoomOut.fontSize = 35


buttons.append(buttonPlay)
buttons.append(buttonZoomIn)
buttons.append(buttonZoomOut)

LEFT = 1
RIGHT = 3
MOVE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(MOVE_EVENT, 70)
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # left click is for moving or pressing buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if event.button == LEFT:
                if buttonPlay.collidePoint(mouse):
                    play = not play
                    pressPlay(buttonPlay)

                elif buttonZoomIn.collidePoint(mouse):
                    mygrid.zoom(True)

                elif buttonZoomOut.collidePoint(mouse):
                    mygrid.zoom(False)

                else:
                    start = mouse
                    myPivot.updateCenterCoord()
                    dragMove = True

            # Right click is for drawing cells
            elif event.button == RIGHT:
                dragDraw = True
                # cannot draw when mouse on button
                if not pressedButton(buttons, mouse):
                    mouse = pygame.mouse.get_pos()
                    pressedCell = getCellPressed(myPivot, mouse, mygrid.size)
                    mygrid.add(pressedCell)

        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            dragMove = False
            myPivot.transformPivot(mygrid.size)

        if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
            dragDraw = False

        if event.type == MOVE_EVENT and dragMove:
            end = pygame.mouse.get_pos()
            myPivot.move(start, end, mygrid.size)

        if event.type == MOVE_EVENT and dragDraw:
            mouse = pygame.mouse.get_pos()
            pressedCell = getCellPressed(myPivot, mouse, mygrid.size)
            mygrid.add(pressedCell)

        if event.type == UPDATE_EVENT and play:
            mygrid.update()

    printScreen(screen, sizeX, sizeY, mygrid, myPivot, buttons)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(40)